# Python Standard Library Imports
import typing as T
from decimal import Decimal


DecimalTypes = T.Union[str, int, float, Decimal]


class ConversionConstants:
    """Constants for converting between different units of measurement.

    Reference: https://www.nist.gov/system/files/documents/2019/12/03/00-20-h133-apdxE_final-17.pdf  # noqa: E501
    """

    class Distance:
        """Constants for converting between different units of distance.

        The canonical unit is meters.
        """

        # Imperial to Imperial
        MI_TO_FT = Decimal('5280')
        YD_TO_FT = Decimal('3')
        FT_TO_IN = Decimal('12')
        IN_TO_FT = Decimal('1') / FT_TO_IN
        YD_TO_MI = YD_TO_FT / MI_TO_FT

        # Imperial to Metric
        IN_TO_M = Decimal('0.0254')
        FT_TO_M = Decimal('0.3048')
        YD_TO_M = Decimal('0.9144')
        MI_TO_M = Decimal('1609.347')

        # Metric to Metric
        M_TO_MM = Decimal('1000')
        M_TO_CM = Decimal('100')
        M_TO_M = Decimal('1')
        M_TO_KM = Decimal('0.001')

        MM_TO_M = Decimal('0.001')
        CM_TO_M = Decimal('0.01')
        KM_TO_M = Decimal('1000')

        # Metric to Imperial
        M_TO_FT = Decimal('1.0') / FT_TO_M
        M_TO_IN = Decimal('1.0') / IN_TO_M
        M_TO_YD = Decimal('1.0') / YD_TO_M
        # M_TO_MI = Decimal('1.0') / MI_TO_M
        M_TO_MI = Decimal('0.0006213712')  # NIST value

    class Weight:
        """Constants for converting between different units of weight.

        The canonical unit is grams.
        """

        # Imperial to Imperial
        LB_TO_OZ = Decimal('16')
        OZ_TO_LB = Decimal('0.0625')

        # Metric to Imperial
        G_TO_OZ = Decimal('0.03527396')
        G_TO_LB = G_TO_OZ * OZ_TO_LB
        KG_TO_OZ = Decimal('35.27396')
        KG_TO_LB = Decimal('2.204623')

        # Imperial to Metric
        OZ_TO_G = Decimal('1.0') / G_TO_OZ
        LB_TO_G = LB_TO_OZ * OZ_TO_G
        OZ_TO_KG = Decimal('1.0') / KG_TO_OZ

        # Metric to Metric
        G_TO_KG = Decimal('0.001')
        KG_TO_G = Decimal('1000')


def convert_unit(value: DecimalTypes, conversion_constant: DecimalTypes) -> Decimal:
    return Decimal(value) * Decimal(conversion_constant)
