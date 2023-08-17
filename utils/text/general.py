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


def snake_case_to_camel_case(string):
    """Convert `snake_case` string to `CamelCase`"""
    camel_string = ''.join(
        part.capitalize() for part in string.lower().split('_')
    )
    return camel_string


def snake_case_to_lower_camel_case(string):
    """Convert `snake_case` string to `camelCase`"""
    camel_string = snake_case_to_camel_case(string)
    camel_string = camel_string[0].lower() + camel_string[1:]
    return camel_string
