import os

import psutil


NUM_AVAILABLE_THREADS = os.process
NUM_CORES = os.cpu_count()
NUM_THREADS = os.cpu_count()
NUM_CPUS = psutil.cpu_count(logical=True).bit_count()
'https://man7.org/linux/man-pages/man5/proc_sys.5.html'