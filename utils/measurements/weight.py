# Python Standard Library Imports
from decimal import Decimal

# Local Imports
from .units import (
    AbstractMeasurement,
    ConversionConstants,
    convert_unit,
)


C = ConversionConstants.Weight


class WeightType(AbstractMeasurement):
    """Class that represents weight.

    Canonical unit is in grams.
    """

    @classmethod
    def from_grams(cls, value: Decimal) -> 'WeightType':
        return cls(value)

    @classmethod
    def from_kilograms(cls, value: Decimal) -> 'WeightType':
        return convert_unit(value, C.KG_TO_G, cls)

    @classmethod
    def from_pounds(cls, value: Decimal) -> 'WeightType':
        return convert_unit(value, C.LB_TO_G, cls)

    ##
    # NOTE: Lots of helper function follow, sorting rules:
    #
    # 1. Metric (SI), then Imperial
    # 2. Increasing unit sizes
    #

    @property
    def g(self) -> 'WeightType':
        return self

    @property
    def kg(self) -> 'WeightType':
        return convert_unit(self, C.G_TO_KG, self.__class__)

    @property
    def oz(self) -> 'WeightType':
        return convert_unit(self, C.G_TO_OZ, self.__class__)

    @property
    def lb(self) -> 'WeightType':
        return convert_unit(self, C.G_TO_LB, self.__class__)
