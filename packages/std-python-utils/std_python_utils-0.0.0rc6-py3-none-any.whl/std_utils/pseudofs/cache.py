import asyncio
import logging
import os
import typing
from asyncio import TaskGroup

import aiofile


asyncio.get_event_loop()
sysfs_cpu_dir = '/sys/devices/system/cpu'
l1_cache_dir = 'index0'
l2_cache_dir = 'index1'
l3_cache_dir = 'index2'
l4_cache_dir = 'index3'
cache_dirs = (l1_cache_dir, l2_cache_dir, l3_cache_dir, l4_cache_dir)

cache_info_files = (
    'id',
    'level',
    'type',
    'size',
    'coherency_line_size',
    'number_of_sets',
    'ways_of_associativity',
    'shared_cpu_list',
    'shared_cpu_map',
    'physical_line_partition'
)


class CPUCacheLevelInfo(typing.NamedTuple):
    '''
    id: Cache ID
    level: Cache level
    type: Cache type
    size: Total cache size
    coherency_line_size: Coherency line size
    number_of_sets: Number of sets
    '''
    id: int
    level: int
    type: str
    size: int
    coherency_line_size: int
    number_of_sets: int
    ways_of_associativity: int
    shared_cpu_list: typing.Set[int]
    shared_cpu_map: str
    physical_line_partition: int


class CPUInfo(typing.NamedTuple):
    id: int
    cache_info: tuple[CPUCacheLevelInfo, ...]


def is_cpu_dir(dir_name: str) -> bool:
    return dir_name.startswith('cpu') and dir_name[-1].isnumeric()


def get_cpu_list():
    cpu_list = tuple(filter(is_cpu_dir, os.listdir(sysfs_cpu_dir)))
    return cpu_list


async def read_data_from_file(file_path: str):
    logging.debug(f'Reading data from {file_path}')
    async with aiofile.async_open(file_path, 'r') as afp:
        data = (await afp.read()).rstrip()
        logging.debug(f'Read data from {file_path}:\n{data}')
        return data


async def get_cache_cpu_level_info(cache_dir: str):
    coros = (
        read_data_from_file(f'{cache_dir}/{file}') for file in cache_info_files
    )
    return tuple(await asyncio.gather(*coros))


def get_shared_cpu_list(cpu_list_str: str):
    if '-' in cpu_list_str:
        start, end = map(int, cpu_list_str.split('-'))
        return set(range(start, end + 1))
    if cpu_list_str.isnumeric():
        return {int(cpu_list_str)}

    raise ValueError(
        f'Invalid hex or `-` separated numbers: {cpu_list_str}'
    )


def construct_cpu_cache_level_data(
    data: tuple[
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str
]):
    cpu_id = int(data[0])
    cache_level = int(data[1])
    cache_type = data[2]
    total_cache_size = int(data[3][:-1])
    cache_line_size = int(data[4])
    number_of_sets = int(data[5])
    ways_of_associativity = int(data[6])
    shared_cpu_list_str = data[7]
    shared_cpu_list = get_shared_cpu_list(shared_cpu_list_str)
    shared_cpu_map = data[8]
    physical_line_partition = int(data[9])
    return CPUCacheLevelInfo(
        cpu_id,
        cache_level,
        cache_type,
        total_cache_size,
        cache_line_size,
        number_of_sets,
        ways_of_associativity,
        shared_cpu_list,
        shared_cpu_map,
        physical_line_partition
    )


def is_cache_level_dir(dir_name: str) -> bool:
    key_prefix = 'index'
    starts_with_prefix = dir_name.startswith(key_prefix)
    numeric_end = dir_name[len(key_prefix):].isnumeric()
    return starts_with_prefix and numeric_end


def get_sysfs_cpu_cache_dirs(cpu_name: str) -> tuple[str, ...]:
    base_cache_dir = '/'.join((sysfs_cpu_dir, cpu_name, 'cache'))
    cache_level_dirs = filter(
        lambda dir_name: is_cache_level_dir(dir_name),
        os.listdir(base_cache_dir)
    )
    return tuple(
        '/'.join((base_cache_dir, cache_level_dir))
        for cache_level_dir in cache_level_dirs
    )


async def get_cache_cpu_info(cpu_name: str):
    sysfs_cpu_cache_dirs = get_sysfs_cpu_cache_dirs(cpu_name)
    logging.debug(f'CPU: {cpu_name} has cache dirs: {sysfs_cpu_cache_dirs}')
    async with TaskGroup() as tg:
        cache_tasks = tuple(
            tg.create_task(get_cache_cpu_level_info(cache_dir))
            for cache_dir in sysfs_cpu_cache_dirs
        )
    results = tuple(task.result() for task in cache_tasks)
    return tuple(
        construct_cpu_cache_level_data(data)
        for data in results
    )


async def get_all_cpu_info():
    cpu_list = get_cpu_list()
    async with TaskGroup() as tg:
        cpu_tasks = tuple(
            tg.create_task(get_cache_cpu_info(cpu))
            for cpu in cpu_list
        )
    results = tuple(task.result() for task in cpu_tasks)

    return tuple(
        CPUInfo(
            id=int(cpu.split('cpu')[-1]),
            cache_info=cache_info
        )
        for cpu, cache_info in zip(cpu_list, results)
    )




