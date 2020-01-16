# HTK Imports
from htk.utils.enums import get_enum_symbolic_name


def get_unit_type_choices():
    from htk.apps.addresses.enums import AddressUnitType
    choices = [(unit_type.value, get_enum_symbolic_name(unit_type),) for unit_type in AddressUnitType]
    return choices
