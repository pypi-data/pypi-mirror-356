from typing import cast

import numpy as np

LinearNpArray = np.ndarray[1, int]

def ofastrange(stop: int):
    i = -1
    while i < stop:
        yield i
        i += 1
list().__setitem__()
def fast_range( stop: int = None) -> LinearNpArray:
    return np.linspace(
        start=0,
        stop=stop,
        num=1,
        dtype=int
    )



