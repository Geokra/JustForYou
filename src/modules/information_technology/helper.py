
from enum import Enum


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

