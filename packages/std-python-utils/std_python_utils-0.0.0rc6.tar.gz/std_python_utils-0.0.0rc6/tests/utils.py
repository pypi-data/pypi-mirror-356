import asyncio
from typing import Any, Coroutine, Optional


class Expectation:
    expecting: bool = False
    expected: Optional[Any] = None

    def __init__(
        self, expecting: bool = False, expectation: Optional[Any] = None
    ):
        self.expecting = expecting
        self.expected = expectation


def sync_test_coro(
    corofunc: Coroutine,
    coro_args: Optional[tuple] = None,
    coro_kwargs: Optional[dict] = None
) -> Any:
    has_args = coro_args is not None and len(coro_args) > 0
    has_kwargs = coro_kwargs is not None and len(coro_kwargs) > 0

    if has_args and has_kwargs:
        coro = corofunc(*coro_args, **coro_kwargs)
    elif has_args:
        coro = corofunc(*coro_args)
    elif has_kwargs:
        coro = corofunc(**coro_kwargs)
    else:
        coro = corofunc()

    return asyncio.run(coro)


def get_benchmark_data(
    coro: Coroutine[Any, Any, tuple],
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None
) -> dict:
    new_benchmark_data = {
        'function_to_benchmark': sync_test_coro, 'corofunc': coro,
    }
    if args:
        new_benchmark_data['coro_args'] = args
    if kwargs:
        new_benchmark_data['coro_kwargs'] = kwargs
    return new_benchmark_data
