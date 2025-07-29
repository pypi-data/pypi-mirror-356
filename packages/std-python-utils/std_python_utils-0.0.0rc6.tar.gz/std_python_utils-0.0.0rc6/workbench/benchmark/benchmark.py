import itertools
import time
import typing
from enum import auto, Enum, StrEnum
from numbers import Number
from typing import Optional
from statistics import mean, stdev, variance
import logging

from std_utils.models.special import CallableInstance, ParamatersInstance, StarmapInstance


class BenchMarkCallType(Enum):
    NO_INPUT = auto()
    ARGS = auto()
    KWARGS = auto()
    ARGS_KWARGS = auto()


class BenchmarkUnits(StrEnum):
    SECONDS = "s"
    MILLISECONDS = "ms"
    MICROSECONDS = "us"
    NANOSECONDS = "ns"


class BenchmarkTiming:
    magnitude: float
    units: BenchmarkUnits

class BenchmarkInput(typing.NamedTuple):
    name: str
    call_type: BenchMarkCallType
    starmap_data: StarmapInstance
    iterations: int = 1
    notes: str = ''


class BenchmarkOutputSummary(typing.NamedTuple):
    params: ParamatersInstance
    iterations: int
    min_time: float
    max_time: float
    avg_time: float
    variance: float
    stdev: float
    results: Optional[tuple[float]] = None

    def print(self) -> str:
        return f'{self.params} Benchmark Summary\n' \
               f'Iterations: {self.iterations}\n' \
               f'Min Time: {get_timing_str(self.min_time)}\n' \
               f'Max Time: {get_timing_str(self.max_time)}\n' \
               f'Avg Time: {get_timing_str(self.avg_time)}\n' \
               f'Variance: {get_timing_str(self.variance)}\n' \



class BenchmarkOutputSummarySet(typing.NamedTuple):
    name: str
    summaries: tuple[BenchmarkOutputSummary]

    def print(self) -> str:
        prefix = f'{self.name} Benchmark Summary\n'
        separator = '-' * 20 + '\n'
        return prefix + separator.join(map(lambda summary: summary.print(), self.summaries))



def get_units_from_ns(time_ns: Number) -> tuple[Number, BenchmarkUnits]:
    time_ms = time_ns * 1e-6
    time_us = time_ns * 1e-3
    time_s = time_ns * 1e-9
    benchmark_unit: BenchmarkUnits
    report_time: Number
    if time_s >= 1:
        report_time, benchmark_unit = time_s, BenchmarkUnits.SECONDS
    elif time_ms >= 1:
        report_time, benchmark_unit = time_ms, BenchmarkUnits.MILLISECONDS
    elif time_us >= 1:
        report_time, benchmark_unit = time_us, BenchmarkUnits.MICROSECONDS
    else:
        report_time, benchmark_unit = time_ns, BenchmarkUnits.NANOSECONDS
    return report_time, benchmark_unit


def get_timing_str(time_ns: int) -> BenchmarkTiming:
    duration, units = get_units_from_ns(time_ns)

    return f'{duration} {units}'


def benchmark_funcdata(func_data: CallableInstance, call_type: BenchMarkCallType) -> int:
    logging.debug(f'Benchmarking: {func_data} with call type: {call_type}')
    match call_type:
        case BenchMarkCallType.NO_INPUT:
            start = time.perf_counter_ns()
            func_data.func()
            end = time.perf_counter_ns()
        case BenchMarkCallType.ARGS:
            start = time.perf_counter_ns()

            func_data.func(*func_data.params.args)
            end = time.perf_counter_ns()
        case BenchMarkCallType.KWARGS:
            start = time.perf_counter_ns()
            func_data.func(**func_data.params.kwargs)
            end = time.perf_counter_ns()
        case BenchMarkCallType.ARGS_KWARGS:
            start = time.perf_counter_ns()
            func_data.func(*func_data.params.args, **func_data.params.kwargs)
            end = time.perf_counter_ns()
        case _:
            raise ValueError(f"Invalid call type: {call_type}")

    return (end - start)





def benchmark_func_on_input(
    func_data: CallableInstance,
    call_type: BenchMarkCallType,
    iterations: int,
    full: bool = False
) -> float:
    logging.debug(f'Benchmark input: {func_data} for {iterations} iterations with call type: {call_type}')

    benchmark_iterable = tuple(zip(itertools.repeat(func_data, iterations), itertools.repeat(call_type, iterations)))
    logging.debug(f'Benchmark iterable: {benchmark_iterable[0]}')

    results = tuple(itertools.starmap(benchmark_funcdata, benchmark_iterable))
    logging.debug(f'Benchmark Results: {tuple(results)}')
    summary_results = results if full else None
    return BenchmarkOutputSummary(
        params=func_data.params,
        iterations=iterations,
        min_time=min(results),
        max_time=max(results),
        avg_time=mean(results),
        variance=variance(results),
        stdev=stdev(results),
        results=summary_results
    )


def benchmark(benchmark_input: BenchmarkInput, full: bool = False) -> BenchmarkOutputSummary:
    baseline_start, baseline_end = time.perf_counter_ns(), time.perf_counter_ns()
    resolution = (baseline_end - baseline_start)
    resolution_str = get_timing_str(resolution)
    logging.debug(f'Time resolution: {resolution} s')
    func_benchmark_data = zip(
        benchmark_input.starmap_data.get_callable_instances(),
        itertools.repeat(benchmark_input.call_type),
        itertools.repeat(benchmark_input.iterations),
        itertools.repeat(full)
    )
    return BenchmarkOutputSummarySet(
        name=benchmark_input.name,
        summaries=itertools.starmap(benchmark_func_on_input, func_benchmark_data)
    )


