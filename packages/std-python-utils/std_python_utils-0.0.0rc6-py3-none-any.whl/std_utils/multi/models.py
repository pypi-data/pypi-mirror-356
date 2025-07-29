import traceback
import tracemalloc
from collections.abc import Callable
from tracemalloc import Frame, Traceback

from std_utils.models.bases import BaseModel


class TaskCallCaller(BaseModel):
    caller: Callable
    frametype: Frame

class TaskExecution(BaseModel):
    caller: Callable
    frame: Frame
    tb: Traceback
class TaskInvocation(BaseModel):
    pass


class TaskCall(BaseModel):
    caller: Callable
    frame: Frame
    tb: Traceback


class Task(BaseModel):
    caller: Callable
    func: Callable
    args: tuple = ()
    kwargs: dict = {}


def inner():
    stack = traceback.extract_stack(limit=1)
    tb = traceback.extract_tb(tracemalloc.get_object_traceback(stack))
    gkeys = list(globals().keys())
    lkeys = list(locals().keys())
    gs = globals()
    print('loader', gs['__loader__'])
    print(set(gkeys + lkeys))
    return stack, tb
def outer():
    return inner()

output = outer()
