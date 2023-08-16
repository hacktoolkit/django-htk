# Python Standard Library
# Python Standard Library Imports
import typing as t
from functools import reduce


def replace(data, replacements: t.List[t.Tuple[str, str]]):
    """
    Allows to perform several string substitutions.

    This function performs several string replacements on the initial `data`
    string using a list of 2-iterables `(old, new)`.
    """
    return reduce(
        lambda string, replacement: string.replace(*replacement),
        replacements,
        data,
    )
