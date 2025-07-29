from types import SimpleNamespace

doc_version = '3.14'
object_instance_attributes = [
    '__class__', # 3.2.11.1
    '__delattr__', # 3.3.2
    '__dir__',  # 3.3.2
    '__doc__', # Not documented
    '__eq__',  # 3.3.2
    '__format__',  # 3.3.1
    '__ge__',  # 3.3.1
    '__getattribute__',  # 3.3.2
    '__getstate__',
    '__gt__',  # 3.3.1
    '__hash__', # 3.3.1
    '__init__', # 3.3.1
    '__init_subclass__',  # 3.3.3
    '__le__',  # 3.3.1
    '__lt__',  # 3.3.1
    '__ne__',  # 3.3.1
    '__new__',  # 3.3.1
    '__reduce__', # [1] pickle -> Pickling Class Instances -> Persistence of External objects
    '__reduce_ex__', #[1]
    '__repr__',  # 3.3.1
    '__setattr__',  # 3.3.2
    '__sizeof__', # Not documented
    '__str__',  # 3.3.1
    '__subclasshook__' # Undocumented but findable in docs abc -> ABCMeta -> __sublcasshook__()
]