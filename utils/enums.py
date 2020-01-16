# Python Standard Library Imports

# HTK Imports
from htk.utils import htk_setting


def enum_to_str(enum_obj):
    """Converts an enum.Enum to a string
    """
    value = ' '.join([word.capitalize() for word in enum_obj.name.split('_')])
    return value


def get_enum_symbolic_name(enum_obj):
    """Gets the symbolic name of an enum.Enum object

    Uses `enum_to_str()` unless an override is defined
    """
    overrides = htk_setting('HTK_ENUM_SYMBOLIC_NAME_OVERRIDES', {})
    key = str(enum_obj)
    if key in overrides:
        symbolic_name = overrides[key]
    else:
        symbolic_name = enum_to_str(enum_obj)
    return symbolic_name


def get_enum_choices(enum_class):
    choices = [
        (en.value, get_enum_symbolic_name(en),)
        for en
        in enum_class
    ]
    return choices
