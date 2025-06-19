# Python Standard Library Imports
from enum import Enum

# HTK Imports
from htk.compat import has_min_python_version
from htk.utils import htk_setting


# isort: off


class HtkEnum(Enum):
    @property
    def display(self):
        return get_enum_symbolic_name(self)

    def json_encode(self):
        """json_encode Generate a valid dict for JSON

        Given enum item is converted to a dict that is encodable to JSON.

        Returns:
            dict: { 'name': str, 'value': int, 'isHidden': bool }
        """
        payload = {
            'name': enum_to_str(self),
            'value': self.value,
            'isHidden': (
                self.is_hidden() if hasattr(self, 'is_hidden') else False
            ),
        }
        return payload

    @classmethod
    def choices(cls):
        """choices Dict of enum items

        An helper method to easily build enum into a `dict`. This dict can be
        used easily pass to JS frameworks.

        Returns:
            dict: { [NAME]: { 'name': str, 'value': int, 'isHidden': bool } }
        """
        choices = {_enum.name: _enum.json_encode() for _enum in cls}
        return choices


def enum_to_str(enum_obj):
    """Converts an enum.Enum to a string"""
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


def get_enum_choices(enum_class, include_hidden=False):
    choices = [
        (
            en.value,
            get_enum_symbolic_name(en),
        )
        for en in enum_class
        if (
            include_hidden
            or (
                not include_hidden
                and (not hasattr(en, 'is_hidden') or not en.is_hidden())
            )
        )
    ]
    return choices


def build_enum_data(enum_class):
    enum_data = [
        {
            'name': get_enum_symbolic_name(en),
            'value': en.value,
            'is_hidden': hasattr(en, 'is_hidden') and en.is_hidden(),
        }
        for en in enum_class
    ]
    return enum_data


if has_min_python_version(3, 6):
    from enum import IntFlag

    class HtkIntFlag(IntFlag):
        """ HTK IntFlag

        Wrapper around Python's built-in `enum.IntFlag` to provide extra
        functionalities.

        Requires: Python 3.6 or greater
        Reference: https://docs.python.org/3.6/library/enum.html#enum.IntFlag
        """
        @classmethod
        def list_flags(cls, int_value):
            """List Flags

            Returns the list of flags that value contains, running bitwise
            `&` (and) operator against the value.
            """
            flags = [flag for flag in cls if int_value & flag > 0]
            return flags
