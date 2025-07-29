pypool
-------
An extensive python resource pool implementation

### Installation

```
pip install pypool3
```

### Examples

```python
from pypool import Pool

numbers = iter(range(0, 1000))
factory = lambda: next(numbers)

pool = Pool(factory, max_size=100)
for _ in range(0, 10):
    with pool.reserve() as number:
        print(number)
```
