from collections.abc import Callable, Iterable
from typing import Any


def tuplemap(func: Callable, iterable: Iterable[Any], *iterables: Any) -> tuple:
    '''Apply a function to each item of an iterable and return a tuple of the results.'''
    return tuple(map(func, iterable, *iterables))