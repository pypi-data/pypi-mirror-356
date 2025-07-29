import re
from typing import Final
from re import Pattern


cpuinfo_keys = (
'address_sizes', 'apicid', 'bogomips', 'bugs', 'cache_alignment', 'cache_size',
'clflush_size', 'core_id', 'cpu_MHz', 'cpu_cores', 'cpu_family', 'cpuid_level',
'flags', 'fpu', 'fpu_exception', 'initial_apicid', 'microcode', 'model',
'model_name', 'physical_id', 'power_management', 'processor', 'siblings',
'stepping', 'vendor_id', 'vmx_flags', 'wp')

_address_sizes_pattern: Final[Pattern] = re.compile(
    r'\d{1,3} bits physical, \d{1,3} bits virtual'
)
_cache_size_pattern: Pattern = re.compile(r'\d+ KB')
_word_list_pattern: Pattern = re.compile(r'[\w\s]+')