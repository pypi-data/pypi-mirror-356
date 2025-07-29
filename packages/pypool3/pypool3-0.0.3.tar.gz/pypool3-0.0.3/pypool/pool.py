"""
Extensive Generic Resource-Pool Implementation

original design inspired by https://github.com/Bogdanp/resource_pool
"""
import time
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Type, TypeVar, Generic, Callable, Optional, Generator, Tuple
from typing_extensions import Self

#** Variables **#
__all__ = [
    'PoolError',
    'Empty',
    'Full',
    'Timeout',

    'Pool',
]

T = TypeVar('T')

#** Classes **#

class PoolError(Exception):
    pass

class Empty(PoolError):
    pass

class Full(PoolError):
    pass

class Timeout(PoolError):
    pass

@dataclass(repr=False)
class Pool(Generic[T]):
    factory:    Callable[[], T]
    max_size:   Optional[int]   = None
    min_size:   Optional[int]   = None
    expiration: Optional[float] = None
    timeout:    Optional[float] = None
    cleanup:    Callable[[T], None] = lambda _: None

    def __post_init__(self):
        self.pool       = []
        self.pool_size  = 0
        self.condition  = threading.Condition()
        self.min_size   = self.min_size or self.max_size
        self.next_clean = self.expiration + time.time() \
            if self.expiration else None

    def _append(self, item: T):
        """append item w/ expiration (if enabled)"""
        expr = self.expiration + time.time() if self.expiration else None
        self.pool.append((item, expr))
        self.condition.notify() # notify pool new resource is available

    def _remove(self, item: T):
        """remove item from pool and untrack it"""
        self.pool_size = max(0, self.pool_size - 1)
        self.cleanup(item)
        self.condition.notify()

    def _check(self,
        entry:  Tuple[T, float],
        now:    Optional[float] = None,
        remove: bool = False,
    ) -> Optional[T]:
        """check to see if item is expired and remove it if expired"""
        item, expr = entry
        if expr:
            now = now or time.time()
            if expr <= now:
                if remove:
                    self.pool.remove(entry)
                item = self._remove(item)
        return item

    def __repr__(self):
        cname = self.__class__.__name__
        return '{}(min={}, max={}, expr={}, timeout={})'.format(
            cname, self.min_size, self.max_size, self.expiration, self.timeout)

    def __enter__(self) -> Self:
        """pass self on context-manager"""
        return self

    def __exit__(self, *_):
        """ensure all items are drained on pool-exit"""
        self.drain()

    def get(self, block: bool = True, timeout: Optional[float] = None) -> T:
        """
        retrieve a single item from the resource-pool

        :param block:   wait for an item and block until one is found
        :param timeout: timeout on block in seconds (if enabled)
        :return:        item from resource-pool
        """
        item    = None
        timeout = timeout or self.timeout
        with self.condition:
            while item is None:
                # remove expired items from pool w/ periodic pool cleanup
                if self.expiration and self.next_clean:
                    now = time.time()
                    if self.next_clean <= now:
                        for entry in self.pool:
                            self._check(entry, now, remove=True)
                        self.next_clean = now + self.expiration
                # spawn more items while pool is under-sized
                # or if max-size is never specified and pool is empty
                while (self.min_size and self.pool_size < self.min_size) \
                    or (not self.max_size and not len(self.pool)):
                    self.pool_size += 1
                    new_item = self.factory()
                    self._append(new_item)
                # wait until a resource is available
                while not self.pool:
                    if block:
                        if not self.condition.wait(timeout):
                            raise Timeout('GET', timeout)
                    elif not len(self.pool):
                        raise Empty
                # pull resource and discard to try-again if expired
                item = self._check(self.pool.pop())
            return item

    def put(self, item: T, block: bool = True, timeout: Optional[float] = None):
        """
        place item back into resource-pool for later reuse

        :param item:    item to place back into resource-pool
        :param block:   block to place into pool if pool is full
        :param timeout: timeout on block in seconds (if enabled)
        """
        timeout = timeout or self.timeout
        with self.condition:
            # wait until item can be added to pool
            while self.max_size and len(self.pool) >= self.max_size:
                if block:
                    if not self.condition.wait(timeout):
                        raise Timeout('PUT', timeout)
                elif len(self.pool) >= self.max_size:
                    raise Full
            # append item to pool w/ expiration
            self._append(item)

    def get_nowait(self) -> T:
        """
        alias for getting item without any blocking or timeout
        """
        return self.get(block=False)

    def put_nowait(self, item: T):
        """
        alias for putting item without any blocking or timeout
        """
        return self.put(item, block=False)

    def discard(self, item: T):
        """
        notify pool to untrack a single item from pool

        :param item: item to untrack from pool
        """
        with self.condition:
            self._remove(item)

    @contextmanager
    def reserve(self,
        timeout:    Optional[float] = None,
        discard_on: Tuple[Type[Exception], ...] = (),
    ) -> Generator[T, None, None]:
        """
        reserve an item from the queue and place it back after usage

        :param timeout:    timeout on block in seconds
        :param discard_on: discard item rather than put in pool on exceptions
        :return:           temporary access to pool resource
        """
        discard = False
        item  = self.get(timeout=timeout)
        try:
            yield item
        except discard_on as err:
            discard = True
            self.discard(item)
            raise err
        finally:
            if not discard:
                self.put(item, timeout=timeout)

    def drain(self):
        """
        wait until all items have been discarded and cleaned up from pool
        """
        while self.pool_size > 0:
            item = self.get(block=True)
            with self.condition:
                self._remove(item)

