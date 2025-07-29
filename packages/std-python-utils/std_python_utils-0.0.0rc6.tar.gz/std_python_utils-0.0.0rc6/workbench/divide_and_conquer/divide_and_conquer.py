from collections.abc import Collection, list_iterator, Sized
from numbers import Number
from typing import Optional


list_iterator
auto_min_size = 1000000
#maybe sized
def dac_parallel_sum(
    iterable: Collection[Number],
    min_size: Optional[int]=None
) -> Number:
    """Sum all elements in an iterable."""
    if min_size is None:
        min_size = auto_min_size
    if len(iterable) <= min_size:
        return sum(iterable)

    midpoint = len(iterable) // 2
    return dac_parallel_sum([iterable[:midpoint], iterable[midpoint:]])
