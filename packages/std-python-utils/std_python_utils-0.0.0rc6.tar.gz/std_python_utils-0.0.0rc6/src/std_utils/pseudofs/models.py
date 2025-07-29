import re
from collections import OrderedDict
from decimal import Decimal
from enum import auto, StrEnum
from fractions import Fraction
from numbers import Integral, Number, Rational, Real
from re import Pattern
from typing import Any, ClassVar, Final, Literal
OrderedDict
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator, GetCoreSchemaHandler, model_validator, TypeAdapter)
from pydantic.alias_generators import to_pascal
from pydantic_core import core_schema, CoreSchema


features = {}

def get_cache_strings_config():
    if 'low_memory' in features:
        return 'none'

    return 'all'

CONFIG_CACHE_STRINGS: Final[str] = get_cache_strings_config()

class FractionModel(Fraction):
    @classmethod
    def from_decimal(cls, dec: Decimal) -> 'FractionModel':
        return cls(dec)

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: Any,
        handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.float_schema()

class Measurement(BaseModel):
    #model_config = ConfigDict(arbitrary_types_allowed=True)
    value: FractionModel
    unit: str

    @field_validator('value', mode='before')
    def _validate_fraction(cls, value: Number) -> Fraction:
        try:
            return FractionModel(value)
        except ValueError:
            raise ValueError(
                f"Value must be a valid rational number. Found: {value}"
            )








class MemoryUnit(StrEnum):
    BIT = "bit"
    BYTE = "byte"
    KB = auto()
    KIB = "kib"
    MB = "mb"
    MIB = "mib"
    GB = "gb"
    GIB = "gib"
    TB = "tb"
    TIB = "tib"
    PB = "pb"
    PIB = "pib"



class MemoryMeasurement(Measurement):
    unit: MemoryUnit
    value: FractionModel


    units_to_bits: ClassVar[dict[MemoryUnit, int]] = {
            MemoryUnit.BIT: 1,
            MemoryUnit.BYTE: 8,
            MemoryUnit.KB: 8 * 10 ** 3,
            MemoryUnit.KIB: 8 * 2 ** 10,
            MemoryUnit.MB: 8 * 10 ** 6,
            MemoryUnit.MIB: 8 * 2 ** 20,
            MemoryUnit.GB: 8 * 10 ** 9,
            MemoryUnit.GIB: 8 * 2 ** 30,
            MemoryUnit.TB: 8 * 10 ** 12,
            MemoryUnit.TIB: 8 * 2 ** 40,
            MemoryUnit.PB: 8 * 10 ** 15,
            MemoryUnit.PIB: 8 * 2 ** 50,
        }

    @classmethod
    def get_bits(cls, value: FractionModel, units: MemoryUnit) -> Real:
        print(cls.units_to_bits)
        return value * cls.units_to_bits[units]


    @model_validator(mode='before')
    @classmethod
    def value_validator(cls, data: dict) -> dict:
        value= data['value']
        print(MemoryUnit._member_map_)
        unit = MemoryUnit['KB']
        numbits = cls.get_bits(value, unit)
        if not numbits.is_integer():
            raise ValueError("Memory size must be an integer number of bits. Found: {numbits}")
        elif numbits < 0:
            raise ValueError("Memory size must be non-negative")
        return data



    def convert(self, to_unit: MemoryUnit) -> 'MemoryMeasurement':
        """
        Convert memory sizes between different units.

        Parameters:
            value (float): The memory size to convert.
            from_unit (MemoryUnit): The unit of the input value (e.g., MemoryUnit.BIT, MemoryUnit.BYTE, etc.).
            to_unit (MemoryUnit): The unit to convert to (e.g., MemoryUnit.BIT, MemoryUnit.BYTE, etc.).

        Returns:
            float: The converted value.
        """

        # Define conversion factors for base-10 and base-2 units


        # Convert the input value to bits
        value_in_bits: Integral = self.value * self.units_to_bits[self.unit]

        # Convert the value from bits to the target unit
        converted_value = value_in_bits / self.units_to_bits[to_unit]

        return MemoryMeasurement(value=converted_value, unit=to_unit)


def genalias(name: str) -> str:
    underscored_fields = ('cache_alignment', 'vendor_id', 'fpu_exception')
    return name.replace('_', ' ') if name not in underscored_fields else name

class CPUInfoBase(BaseModel):
    model_config = ConfigDict(
        cache_strings=CONFIG_CACHE_STRINGS,
        protected_namespaces=(
            f'model_{prefix}'
            for prefix in 'cdefjprv'
        ),
        alias_generator=genalias
    )
    apicid: int
    bogomips: Decimal
    bugs: str = Field(pattern=_word_list_pattern)
    cache_alignment: int
    clflush_size: int
    core_id: int
    cpu_MHz: Decimal
    cpu_cores: int
    cpu_family: int
    cpuid_level: int
    flags: str = Field(pattern=_word_list_pattern)
    fpu: Literal['yes', 'no']
    fpu_exception: Literal['yes', 'no']
    initial_apicid: int
    model: int
    model_name: str
    physical_id: int
    power_management: str
    processor: int
    siblings: int
    stepping: int
    vendor_id: str = Field(pattern=re.compile(r'\w+'))
    vmx_flags: str
    wp: Literal['yes', 'no']


class CPUInfoInputModel(CPUInfoBase):
    _address_sizes_pattern: ClassVar[Pattern] = re.compile(
        r'\d{1,3} bits physical, \d{1,3} bits virtual'
    )
    _cache_size_pattern: Pattern = re.compile(r'\d+ KB')
    _word_list_pattern: Pattern = re.compile(r'[\w\s]+')
    address_sizes: str = Field(pattern=_address_sizes_pattern)
    cache_size: str = Field(pattern=_cache_size_pattern)
    microcode: int


    @field_validator('microcode', mode='before')
    def _validate_microcode(cls, microcode: str) -> int:
        return int(microcode, 16)


class CPUInfoAddressSizes(BaseModel):
    '''Address sizes in bits'''
    physical: int
    virtual: int


class CPUInfoOutputModel(BaseModel):
    _address_sizes_pattern: ClassVar[Pattern] = re.compile(
        r'\d{1,3} bits physical, \d{1,3} bits virtual'
    )
    _cache_size_pattern: Pattern = re.compile(r'\d+ KB')
    _word_list_pattern: Pattern = re.compile(r'[\w\s]+')
    address_sizes: CPUInfoAddressSizes
    apicid: int
    bogomips: Decimal
    bugs: str = Field(pattern=_word_list_pattern)
    cache_alignment: int
    cache_size: MemoryMeasurement
    clflush_size: int
    core_id: int
    cpu_MHz: Decimal
    cpu_cores: int
    cpu_family: int
    cpuid_level: int
    flags: str = Field(pattern=_word_list_pattern)
    fpu: Literal['yes', 'no']
    fpu_exception: Literal['yes', 'no']
    initial_apicid: int
    model: int
    model_name: str
    physical_id: int
    power_management: str
    processor: int
    siblings: int
    stepping: int
    vendor_id: str = Field(pattern=re.compile(r'\w+'))
    vmx_flags: str
    wp: Literal['yes', 'no']

    @classmethod
    def from_cpu_info_input_model(cls, input_model: CPUInfoInputModel) -> 'CPUInfoOutputModel':
        dat = input_model.cache_size.split()[0]
        cache_size = MemoryMeasurement(
            value=FractionModel.from_decimal(Decimal(dat)),
            unit=MemoryUnit.KB
        )
        split_data = input_model.address_sizes.strip().split()
        address_sizes = CPUInfoAddressSizes(
            physical=int(split_data[0]),
            virtual=int(split_data[3])
        )
        old_info = input_model.model_dump(by_alias=False)
        old_info.update({
            'address_sizes': address_sizes,
            'cache_size': cache_size,
            'microcode': str(input_model.microcode)
        })
        return cls(**old_info)