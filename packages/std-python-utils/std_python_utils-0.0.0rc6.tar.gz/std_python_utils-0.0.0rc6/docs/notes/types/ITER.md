# ITER
Iterators and Iterables

## [Iterator Protocol](http://docs.python.org/3/glossary.html#term-iterator-protocol)
## [Iterator](http://docs.python.org/3/glossary.html#term-iterator)
## [Iterable](http://docs.python.org/3/glossary.html#term-iterable)
## [Optimized Scope](http://docs.python.org/3/glossary.html#term-optimized-scope)

A scope where target local variable names are reliably known to the compiler when the code is compiled, allowing
optimization of read and write access to these names. Note: most interpreter optimizations are
applied to all scopes, only those relying on a known set of local and nonlocal variable names are restricted to
optimized scopes.

The following local namespaces are optimized in this fashion:
- functions
- generators
- coroutines
- comprehensions
- generator expressions

# 🔁 Python Iterables, Iterators, and Generators (Sync & Async)

| Concept / ABC       | Inherits From                | Abstract Methods                                     | Mixin / Common Methods                               | Notes |
|---------------------|------------------------------|------------------------------------------------------|------------------------------------------------------|-------|
| **Iterable**        | —                            | `__iter__()`                                         | —                                                    | Used with `for` loops. |
| **Iterator**        | `Iterable`                   | `__iter__()`, `__next__()`                           | —                                                    | Returned by `iter()`. |
| **Generator**       | `Iterator`                   | `send()`, `throw()`                                  | `__iter__()`, `__next__()`, `close()`                | Created with `yield`. |
| **AsyncIterable**   | —                            | `__aiter__()`                                        | —                                                    | Used in `async for`. |
| **AsyncIterator**   | `AsyncIterable`              | `__aiter__()`, `__anext__()`                         | —                                                    | Returned by `__aiter__()`. |
| **AsyncGenerator**  | `AsyncIterator`              | `asend()`, `athrow()`                                | `__aiter__()`, `__anext__()`, `aclose()`             | Created with `async def` + `yield`. |
| **Coroutine**       | `Awaitable`                  | `send()`, `throw()`                                  | `__await__()`, `close()`                             | Result of calling an `async def` function. |

## 🔤 Subclass Examples and Basic Usage

### ✅ Iterable & Iterator

```python
class Count:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration
        val = self.current
        self.current += 1
        return val

for i in Count(3):
    print(i)
```

### ✅ Generator

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for x in countdown(3):
    print(x)
```

### ✅ AsyncIterable & AsyncIterator

```python
class AsyncCounter:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.current >= self.limit:
            raise StopAsyncIteration
        val = self.current
        self.current += 1
        return val

import asyncio
async def run_async_iter():
    async for i in AsyncCounter(3):
        print(i)

asyncio.run(run_async_iter())
```

### ✅ AsyncGenerator

```python
async def agen():
    for i in range(3):
        yield i

async def run_async_gen():
    async for x in agen():
        print(x)

asyncio.run(run_async_gen())
```

### ✅ Coroutine

```python
async def greet():
    return "Hello from coroutine!"


async def main():
    message = await greet()
    print(message)


import asyncio


asyncio.run(main())
```