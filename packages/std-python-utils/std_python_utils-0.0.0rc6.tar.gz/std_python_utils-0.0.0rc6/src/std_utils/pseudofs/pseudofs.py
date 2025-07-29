from collections import OrderedDict

from pydantic import BaseModel

from models import CPUInfoInputModel
from models import CPUInfoOutputModel


cacheinfo = '/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'

cpuinfo = '/proc/cpuinfo'



def read_cpuinfo():
    with open(cpuinfo) as f:
        return f.read()


def get_cpu_info_dict():
    cpu_data = read_cpuinfo()
    split_data = tuple(tuple(data.strip() for data in line.strip().split(':')) for line in cpu_data.splitlines() if line)
    dict_data = {tup[0]: tup[1] for tup in split_data}
    return CPUInfoInputModel(**dict_data)


print(get_cpu_info_dict())
print(CPUInfoOutputModel.from_cpu_info_input_model(get_cpu_info_dict()))