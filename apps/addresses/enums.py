# Python Standard Library Imports
from enum import Enum


class AddressUnitType(Enum):
    NONE = 0
    APT = 1
    FLOOR = 2
    HASH = 3
    SUITE = 4
    UNIT = 5
