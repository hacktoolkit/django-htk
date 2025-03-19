# Python Standard Library Imports
from decimal import Decimal

# Local Imports
from .units import (
    AbstractMeasurement,
    ConversionConstants,
    convert_unit,
)


C = ConversionConstants.Distance


class DistanceType(AbstractMeasurement):
    """Class that represents a distance (e.g. length, width, height).

    Canonical unit is in meters.
    """

    @classmethod
    def from_meters(cls, value: Decimal) -> 'DistanceType':
        return cls(value)

    @classmethod
    def from_kilometers(cls, value: Decimal) -> 'DistanceType':
        return convert_unit(value, C.KM_TO_M, cls)

    @classmethod
    def from_feet(cls, value: Decimal) -> 'DistanceType':
        return convert_unit(value, C.FT_TO_M, cls)

    @classmethod
    def from_yards(cls, value: Decimal) -> 'DistanceType':
        return convert_unit(value, C.YD_TO_M, cls)

    @classmethod
    def from_miles(cls, value: Decimal) -> 'DistanceType':
        return convert_unit(value, C.MI_TO_M, cls)

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
        return convert_unit(self, C.M_TO_KM, self.__class__)

    @property
    def cm(self) -> 'DistanceType':
        return convert_unit(self, C.M_TO_CM, self.__class__)

    @property
    def mm(self) -> 'DistanceType':
        return convert_unit(self, C.M_TO_MM, self.__class__)

    @property
    def in_(self) -> 'DistanceType':
        return self.inch

    @property
    def inch(self) -> 'DistanceType':
        return convert_unit(self, C.M_TO_IN, self.__class__)

    @property
    def ft(self) -> 'DistanceType':
        return convert_unit(self, C.M_TO_FT, self.__class__)

    @property
    def yd(self) -> 'DistanceType':
        return convert_unit(self, C.M_TO_YD, self.__class__)

    @property
    def mi(self) -> 'DistanceType':
        return convert_unit(self, C.M_TO_MI, self.__class__)
