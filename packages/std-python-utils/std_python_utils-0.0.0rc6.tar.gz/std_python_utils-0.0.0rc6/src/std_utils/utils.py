import subprocess
import time


def hex_cpu_mask_to_cores(hex_mask: str) -> tuple[int, ...]:
    """
    Converts a hexadecimal CPU mask to a tuple of enabled core numbers.

    Args:
        hex_mask (str): A string representing the hexadecimal CPU mask (e.g., "00c00").

    Returns:
        tuple: A tuple of integers representing the enabled CPU cores.
    """
    # Convert hex mask to binary
    binary_mask = bin(int(hex_mask, 16))[2:]

    # Reverse binary string to match CPU bit indexing
    reversed_binary = binary_mask[::-1]

    # Get core indices where the bit is set
    cores = tuple(idx for idx, bit in enumerate(reversed_binary) if bit == '1')

    return cores



def subprocess_seq(size):
    com = ['seq', str(size)]
    a = subprocess.run(com, capture_output=True, text=True)
    data = {
        'stdout': a.stdout,
        'stderr': a.stderr,
        'returncode': a.returncode
    }
    return data
