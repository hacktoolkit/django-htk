# Python Standard Library Imports
from functools import reduce


def is_alpha(c):
    result = ord('A') <= ord(c.upper()) <= ord('Z')
    return result


def is_ascii(c):
    result = 0 <= ord(c) <= 127
    return result


def is_ascii_extended(c):
    result = 128 <= ord(c) <= 255
    return result


def replace_many(s, replacements):
    """Allows to perform several string substitutions.

    This function performs several string replacements on the initial `data`
    string using a list of 2-tuples `(old, new)`.
    """
    value = reduce(
        lambda string, replacement: string.replace(*replacement),
        replacements,
        s,
    )
    return value
