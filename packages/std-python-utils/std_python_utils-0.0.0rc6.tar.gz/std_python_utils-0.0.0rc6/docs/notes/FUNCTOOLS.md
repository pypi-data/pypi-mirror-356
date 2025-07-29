# Functools Module in Python

The `functools` module in Python provides higher-order functions that act on or return other functions. These utilities
facilitate functional programming and help in writing concise and maintainable code.

## Decorators

### `@functools.cache(user_function)`

**Description:**  
Caches the results of the `user_function` to optimize repeated calls with the same arguments. This decorator is useful
for functions with expensive computations that are called multiple times with the same inputs.

**Example Use-Case:**

```python
import functools

@functools.cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Usage
print(fibonacci(10))  # Output: 55
```

### `@functools.cached_property(func)`

**Description:**  
Transforms a method into a property whose value is computed once and then cached as a normal attribute. This is
beneficial for expensive computations that should only be performed once per instance.

**Example Use-Case:**

```python
import functools

class DataSet:
    def __init__(self, data):
        self.data = data

    @functools.cached_property
    def mean(self):
        print("Computing mean...")
        return sum(self.data) / len(self.data)

# Usage
data = DataSet([1, 2, 3, 4, 5])
print(data.mean)  # Output: Computing mean... 3.0
print(data.mean)  # Output: 3.0 (cached, no recomputation)
```

### `@functools.lru_cache(user_function)`

**Description:**  
Decorator that wraps a function with a Least Recently Used (LRU) cache. It stores the results of function calls and
reuses them when the same inputs occur, thus saving computation time.

**Example Use-Case:**

```python
import functools

@functools.lru_cache
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

# Usage
print(factorial(5))  # Output: 120
```

### `@functools.lru_cache(maxsize=128, typed=False)`

**Description:**  
An LRU cache decorator with configurable `maxsize` and `typed` parameters. `maxsize` determines the number of cached
calls; `typed` differentiates cache entries based on the types of the arguments.

**Example Use-Case:**

```python
import functools

@functools.lru_cache(maxsize=32, typed=True)
def power(base, exponent):
    return base ** exponent

# Usage
print(power(2, 3))  # Output: 8
print(power(2.0, 3))  # Output: 8.0 (different cache entry due to 'typed=True')
```

## Advanced

### `functools.partial(func, /, *args, **keywords)`

**Description:**  
Returns a new partial object which behaves like `func` with some arguments fixed. Useful for specializing functions with
common argument values.

**Example Use-Case:**

```python
import functools

def multiply(x, y):
    return x * y

double = functools.partial(multiply, 2)

# Usage
print(double(5))  # Output: 10
```

### `functools.partialmethod(func, /, *args, **keywords)`

**Description:**  
Similar to `functools.partial`, but designed for methods in classes. It allows partial application of arguments to
methods.

**Example Use-Case:**

```python
import functools

class Calculator:
    def power(self, base, exponent):
        return base ** exponent

    square = functools.partialmethod(power, exponent=2)

# Usage
calc = Calculator()
print(calc.square(3))  # Output: 9
```

### `functools.reduce(function, iterable, [initial, ]/)`

**Description:**  
Applies a binary function cumulatively to the items of an iterable, reducing it to a single value. Often used for
aggregating results.

**Example Use-Case:**

```python
import functools

numbers = [1, 2, 3, 4, 5]
sum_numbers = functools.reduce(lambda x, y: x + y, numbers)

# Usage
print(sum_numbers)  # Output: 15
```

### `@functools.singledispatch`

**Description:**  
Transforms a function into a single-dispatch generic function, allowing it to dispatch based on the type of the first
argument. This facilitates function overloading based on argument types.

**Example Use-Case:**

```python
import functools

@functools.singledispatch
def process(value):
    raise NotImplementedError("Unsupported type")

@process.register(int)
def _(value):
    return f"Processing integer: {value}"

@process.register(str)
def _(value):
    return f"Processing string: {value}"

# Usage
print(process(10))    # Output: Processing integer: 10
print(process("hi"))  # Output: Processing string: hi
```

### `functools.singledispatchmethod(func)`

**Description:**  
A variant of `singledispatch` for methods, enabling method overloading based on the type of the first argument.

**Example Use-Case:**

```python
import functools

class Processor:
    @functools.singledispatchmethod
    def process(self, value):
        raise NotImplementedError("Unsupported type")

    @process.register(int)
    def _(self, value):
        return f"Processing integer: {value}"

    @process.register(str)
    def _(self, value):
        return f"Processing string: {value}"

# Usage
processor = Processor()
print(processor.process(10))    # Output: Processing integer: 10
print(processor.process("hi"))  # Output: Processing string: hi
```

### `functools.update_wrapper(wrapper, wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)`

**Description:**  
Updates a wrapper function to look more like the wrapped function by copying attributes such as the module, name,
annotations, and docstring. This is useful when creating decorator functions.

### `@functools.wraps`

**Description:**  
A decorator that applies `functools.update_wrapper` to the decorated function. It simplifies the process of making
decorator functions that preserve the metadata of the original function.

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))  # Output: Calling greet Hello, Alice!
```
