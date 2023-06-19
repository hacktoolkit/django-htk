"""
Flag Enum

Usable in Python >= 3.6

There is no backport for Python 2.7

`auto` is imported to easily import from same file
Ex: `from htk.utils.flags import HtkIntFlag, auto`
"""
from enum import IntFlag, auto  # noqa: F401


class HtkIntFlag(IntFlag):
    """HTK Int Flag Enum

    Provides extra functionalities to Python's built-in IntFlag enum type
    """
    @classmethod
    def list_flags(cls, value: int):
        """Extract Flags

        Returns: list of the bitwise or'ed combination.
        """
        flag_list = [flag for flag in cls if value & flag > 0]
        return flag_list
