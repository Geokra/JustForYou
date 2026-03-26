
from enum import Enum, IntEnum


def calculate_storage(width: int, height: int, color_depth: int, frames: int = 1):
    return width * height * color_depth * frames

class Unit(Enum):
    BIT = 0,
    BYTE = 1,
    KIB = 2,
    MIB = 3,
    GIB = 4,
    TIB = 5


BITS_PER_UNIT = {
    Unit.BIT: 1,
    Unit.BYTE: 8,
    Unit.KIB: 8 * 1024,
    Unit.MIB: 8 * 1024**2,
    Unit.GIB: 8 * 1024**3,
    Unit.TIB: 8 * 1024**4,
}

def convert_to_unit(value: int, source_unit: Unit, target_unit: Unit) -> float:
    value_in_bits = value * BITS_PER_UNIT[source_unit]
    return value_in_bits / BITS_PER_UNIT[target_unit]


class Base(IntEnum):
    BINARY = 2
    OCTAL = 8
    TERNARY = 3
    DECIMAL = 10

def convert_number(number: str, from_base: Base, to_base: Base) -> str:
    decimal_number = int(number, from_base)

    if to_base == Base.DECIMAL:
        return str(decimal_number)
    elif to_base == Base.BINARY:
        return bin(decimal_number)[2:]
    elif to_base == Base.TERNARY:
        result = ""
        if decimal_number == 0:
            return "0"
        while decimal_number > 0:
            result = str(decimal_number % 3) + result
            decimal_number //= 3
        return result
    elif to_base == Base.OCTAL:
        return oct(decimal_number)[2:]
    else:
        raise ValueError("Supported bases are 2, 3, 8, and 10.")

def convert_data_units(value, from_unit, to_unit):
    binary_units = {
        'B': 1,
        'KiB': 1024,
        'MiB': 1024**2,
        'GiB': 1024**3,
        'TiB': 1024**4
    }
    
    decimal_units = {
        'B': 1,
        'KB': 1000,
        'MB': 1000**2,
        'GB': 1000**3,
        'TB': 1000**4
    }
    
    if from_unit in binary_units:
        bytes_value = value * binary_units[from_unit]
    elif from_unit in decimal_units:
        bytes_value = value * decimal_units[from_unit]
    else:
        raise ValueError(f"Unbekannte Einheit: {from_unit}")
    
    if to_unit in binary_units:
        result = bytes_value / binary_units[to_unit]
    elif to_unit in decimal_units:
        result = bytes_value / decimal_units[to_unit]
    else:
        raise ValueError(f"Unbekannte Einheit: {to_unit}")
    
    return result