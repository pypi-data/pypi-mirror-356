import collections
import contextlib
import itertools
import operator
from collections.abc import Callable, Iterator, Sequence, Iterable
from typing import Any, Optional, Unpack

from annotated_types import Predicate


def is_true(x: Any) -> bool:
    return bool(x)

a: Predicate = is_true

def take(n: int, iterable: Iterable):
    "Return first n items of the iterable as a list."
    return list(itertools.islice(iterable, n))


def prepend(value: Any, iterable: Iterable):
    "Prepend a single value in front of an iterable."
    # prepend(1, [2, 3, 4]) → 1 2 3 4
    return itertools.chain([value], iterable)


def tabulate(func: Callable, start: int = 0):
    "Return function(0), function(1), ..."
    return map(func, itertools.count(start))


def repeatfunc(func: Callable, times=None, *args):
    "Repeat calls to func with specified arguments."
    if times is None:
        return itertools.starmap(func, itertools.repeat(args))
    return itertools.starmap(func, itertools.repeat(args, times))


def flatten(list_of_lists: Iterable[Iterable]):
    "Flatten one level of nesting."
    return itertools.chain.from_iterable(list_of_lists)


def ncycles(iterable: Iterable, n: int):
    "Returns the sequence elements n times."
    return itertools.chain.from_iterable(itertools.repeat(tuple(iterable), n))


def tail(n: int, iterable: Iterable):
    "Return an iterator over the last n items."
    # tail(3, 'ABCDEFG') → E F G
    return iter(collections.deque(iterable, maxlen=n))


def consume(iterator: Iterator, n: Optional[int] = None):
    "Advance the iterator n-steps ahead. If n is None, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        collections.deque(iterator, maxlen=0)
    else:
        next(itertools.islice(iterator, n, n), None)


def nth(iterable: Iterable, n: int, default: Any = None):
    "Returns the nth item or a default value."
    return next(itertools.islice(iterable, n, None), default)


def quantify(iterable: Iterable, predicate: Callable[[], bool] = bool):
    "Given a predicate that returns True or False, count the True results."
    return sum(map(predicate, iterable))


def first_true(iterable: Iterable, default: bool = False, predicate=None):
    "Returns the first true value or the *default* if there is no true value."
    # first_true([a,b,c], x) → a or b or c or x
    # first_true([a,b], x, f) → a if f(a) else b if f(b) else x
    return next(filter(predicate, iterable), default)


def all_equal(iterable: Iterable, key=None):
    "Returns True if all the elements are equal to each other."
    # all_equal('4٤௪౪໔', key=int) → True
    return len(take(2, itertools.groupby(iterable, key))) <= 1


def unique_justseen(iterable: Iterable, key=None):
    "Yield unique elements, preserving order. Remember only the element just seen."
    # unique_justseen('AAAABBBCCDAABBB') → A B C D A B
    # unique_justseen('ABBcCAD', str.casefold) → A B c A D
    if key is None:
        return map(operator.itemgetter(0), itertools.groupby(iterable))
    return map(next, map(operator.itemgetter(1), itertools.groupby(iterable, key)))


def unique_everseen(iterable: Iterable, key=None):
    "Yield unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') → A B C D
    # unique_everseen('ABBcCAD', str.casefold) → A B c D
    seen = set()
    if key is None:
        for element in itertools.filterfalse(seen.__contains__, iterable):
            seen.add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen.add(k)
                yield element


def unique(iterable: Iterable, key=None, reverse=False):
    "Yield unique elements in sorted order. Supports unhashable inputs."
    # unique([[1, 2], [3, 4], [1, 2]]) → [1, 2] [3, 4]
    return unique_justseen(sorted(iterable, key=key, reverse=reverse), key=key)


def sliding_window(iterable: Iterable, n):
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def grouper(iterable: Iterable, n, *, incomplete='fill', fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks."
    # grouper('ABCDEFG', 3, fillvalue='x') → ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') → ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') → ABC DEF
    iterators = [iter(iterable)] * n
    match incomplete:
        case 'fill':
            return zip_longest(*iterators, fillvalue=fillvalue)
        case 'strict':
            return zip(*iterators, strict=True)
        case 'ignore':
            return zip(*iterators)
        case _:
            raise ValueError('Expected fill, strict, or ignore')


def roundrobin(*iterables: Unpack[Iterable]):
    "Visit input iterables in a cycle until each is exhausted."
    # roundrobin('ABC', 'D', 'EF') → A D E B F C
    # Algorithm credited to George Sakkis
    iterators = map(iter, iterables)
    for num_active in range(len(iterables), 0, -1):
        iterators = cycle(islice(iterators, num_active))
        yield from map(next, iterators)


def subslices(seq: Sequence):
    "Return all contiguous non-empty subslices of a sequence."
    # subslices('ABCD') → A AB ABC ABCD B BC BCD C CD D
    slices = itertools.starmap(slice, itertools.combinations(range(len(seq) + 1), 2))
    return map(operator.getitem, itertools.repeat(seq), slices)


def iter_index(iterable: Iterable, value: Any, start=0, stop=None):
    "Return indices where a value occurs in a sequence or iterable."
    # iter_index('AABCADEAF', 'A') → 0 1 4 7
    seq_index = getattr(iterable, 'index', None)
    if seq_index is None:
        iterator = itertools.islice(iterable, start, stop)
        for i, element in enumerate(iterator, start):
            if element is value or element == value:
                yield i
    else:
        stop = len(iterable) if stop is None else stop
        i = start
        with contextlib.suppress(ValueError):
            while True:
                yield (i := seq_index(value, i, stop))
                i += 1

