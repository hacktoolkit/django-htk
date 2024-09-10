# Python Standard Library Imports
from decimal import Decimal

# Local Imports
from .units import (
    ConversionConstants,
    convert_unit,
)


C = ConversionConstants.Weight


class WeightType(Decimal):
    """Class that represents weight.

    Canonical unit is in grams.
    """

    @classmethod
    def from_grams(cls, value: Decimal) -> 'WeightType':
        return cls(value)

    @classmethod
    def from_kilograms(cls, value: Decimal) -> 'WeightType':
        return cls(convert_unit(value, C.KG_TO_G))

    @classmethod
    def from_pounds(cls, value: Decimal) -> 'WeightType':
        return cls(convert_unit(value, C.LB_TO_G))

    ##
    # NOTE: Lots of helper function follow, sorting rules:
    #
    # 1. Metric (SI), then Imperial
    # 2. Increasing unit sizes
    #

    @property
    def g(self) -> Decimal:
        return self

    @property
    def kg(self) -> Decimal:
        return convert_unit(self, C.G_TO_KG)

    @property
    def oz(self) -> Decimal:
        return convert_unit(self, C.G_TO_OZ)

    @property
    def lb(self) -> Decimal:
        return convert_unit(self, C.G_TO_LB)
