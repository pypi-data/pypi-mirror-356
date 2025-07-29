# oa-utils

Statically typed Python utilities for functional programming.

## Pipeline

This class is useful for programming in the [collection pipeline](https://martinfowler.com/articles/collection-pipeline/) style. It wraps a homogenous variadic tuple and exposes a fluent interface with common functional programming operations. Why a tuple and not a "lazy" iterator? Because a tuple is relatively immutable and because, in my opinion, reified collections are much easier to reason about than stateful iterators (at the expense of performance).

```python
from oa_utils.pipeline import Pipeline

hamming_distance = (
    Pipeline("karolin") # ('k', 'a', 'r', 'o', 'l', 'i', 'n')
    .zip_with(lambda a, b: int(a != b), "kathrin") # (0, 0, 1, 1, 1, 0, 0)
    .sum() # 3
)
```

See [pipeline.py](https://github.com/OlegAlexander/oa-utils/blob/main/oa_utils/pipeline.py) for docstrings and doctests of every method.