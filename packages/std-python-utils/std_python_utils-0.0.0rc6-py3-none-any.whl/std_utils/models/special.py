import itertools
import typing
from typing import Optional
from collections.abc import Iterable, Mapping


class ParamatersInstance(typing.NamedTuple):
    args: Optional[Iterable] = None
    kwargs: Optional[Mapping] = None


MapParametersInstance = Iterable[Iterable]
StarmapParametersInstance = Iterable[ParamatersInstance]


class CallableInstance(typing.NamedTuple):
    func: callable
    params: ParamatersInstance = None


class MapInstance(typing.NamedTuple):
    callable: callable
    param_data: MapParametersInstance

    def get_callable_instances(self) -> Iterable[CallableInstance]:
        return map(CallableInstance, itertools.repeat(self.callable), self.param_data)


class StarmapInstance(typing.NamedTuple):
    callable: callable
    param_data: StarmapParametersInstance

    def get_callable_instances(self) -> Iterable[CallableInstance]:
        return itertools.starmap(
            CallableInstance,
            zip(itertools.repeat(self.callable), self.param_data)
        )
