import os

import pytest

from std_utils.pseudofs import cache
from utils import get_benchmark_data

benchmark_enabled = os.environ.get('BENCHMARK_ENABLED', False)
if benchmark_enabled:
    from pytest_benchmark.fixture import BenchmarkFixture


@pytest.mark.asyncio
async def test_get_all_cpu_info():
    await cache.get_all_cpu_info()


if benchmark_enabled:
    def test_get_all_cpu_info(benchmark: BenchmarkFixture):
        benchmark_data: callable = get_benchmark_data(cache.get_all_cpu_info)
        benchmark(**benchmark_data)
