import cProfile
from functools import wraps
import tracemalloc



def profile_func(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        return result, profiler
    return wrapper


def tracemem_func(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_snapshot = tracemalloc.take_snapshot()
        result = func(*args, **kwargs)
        end_snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()
        return result
    return wrapper