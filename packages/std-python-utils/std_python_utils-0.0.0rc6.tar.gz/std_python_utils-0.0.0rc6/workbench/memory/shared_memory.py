import mmap
from dataclasses import dataclass
from enum import StrEnum
from multiprocessing.shared_memory import SharedMemory
from multiprocessing import Lock
from optparse import Option
from typing import Optional, Set



def os_hint_memory(map_data: mmap.mmap) -> int:
    """Get a hint for the amount of memory to allocate."""
    return 1 << 20  # 1 MiB


class CSHMType(StrEnum):
    RAW_ARRAY = "RAW_ARRAY"
    RAW_VALUE = "RAW_VALUE"
    ARRAY = "ARRAY"
    VALUE = "VALUE"


@dataclass(frozen=True)
class SHMConfig:
    size: int
    name: Optional[str] = None


def create_shared_memory(config: SHMConfig) -> SharedMemory:
    """Get a raw shared memory object."""
    return SharedMemory(name=config.name, create=True, size=config.size)
