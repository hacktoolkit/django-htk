# Python Standard Library Imports
from decimal import Decimal

# Local Imports
from .units import (
    ConversionConstants,
    convert_unit,
)


C = ConversionConstants.Distance


class DistanceType(Decimal):
    """Class that represents a distance (e.g. length, width, height).

    Canonical unit is in meters.
    """

    @classmethod
    def from_meters(cls, value: Decimal) -> 'DistanceType':
        return cls(value)

    @classmethod
    def from_kilometers(cls, value: Decimal) -> 'DistanceType':
        return cls(convert_unit(value, C.KM_TO_M))

    @classmethod
    def from_feet(cls, value: Decimal) -> 'DistanceType':
        return cls(convert_unit(value, C.FT_TO_M))

    @classmethod
    def from_yards(cls, value: Decimal) -> 'DistanceType':
        return cls(convert_unit(value, C.YD_TO_M))

    @classmethod
    def from_miles(cls, value: Decimal) -> 'DistanceType':
        return cls(convert_unit(value, C.MI_TO_M))

    ##
    # NOTE: Lots of helper function follow, sorting rules:
    #
    # 1. Metric (SI), then Imperial
    # 2. Increasing unit sizes
    #

    @property
    def m(self) -> 'DistanceType':
        return self.from_meters(self)

    @property
    def km(self) -> 'DistanceType':
        return self.__class__(convert_unit(self, C.M_TO_KM))

    @property
    def cm(self) -> 'DistanceType':
        return self.__class__(convert_unit(self, C.M_TO_CM))

    @property
    def mm(self) -> 'DistanceType':
        return self.__class__(convert_unit(self, C.M_TO_MM))

    @property
    def in_(self) -> 'DistanceType':
        return self.inch

    @property
    def inch(self) -> 'DistanceType':
        return self.__class__(convert_unit(self, C.M_TO_IN))

    @property
    def ft(self) -> 'DistanceType':
        return self.__class__(convert_unit(self, C.M_TO_FT))

    @property
    def yd(self) -> 'DistanceType':
        return self.__class__(convert_unit(self, C.M_TO_YD))

    @property
    def mi(self) -> 'DistanceType':
        return self.__class__(convert_unit(self, C.M_TO_MI))
