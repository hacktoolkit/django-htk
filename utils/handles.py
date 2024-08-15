# Python Standard Library Imports
import typing as T
from uuid import uuid4

# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.contrib.auth import get_user_model

# HTK Imports
from htk.utils import htk_setting
from htk.utils.text.transformers import seo_tokenize


# isort: off


def _default_unique_across() -> list[T.Tuple[type, str]]:
    """Returns the default list of models and fields that a handle
    must be unique across.

    This is used by `look_up_object_by_unique_handle` and `is_unique_handle`.

    Returns a list of tuples, each containing a model and a field name.
    """
    return [
        (get_user_model(), 'username'),
    ]


def look_up_object_by_unique_handle(
    handle: str,
    unique_across: T.Optional[list[T.Tuple[type, str]]] = None,
) -> T.Optional[type]:
    """Looks up an object by its unique handle across a list of models and fields.

    Returns the object if found, otherwise None.
    """
    if unique_across is None:
        unique_across = _default_unique_across()

    for model, field in unique_across:
        # return the first match
        try:
            obj = model.objects.get(**{field: handle})
            break
        except model.DoesNotExist:
            obj = None

    return obj


def is_unique_handle(
    handle: str,
    unique_across: T.Optional[list[T.Tuple[type, str]]] = None,
) -> bool:
    """Determines whether a handle is unique across a list of models and fields.

    Params:
    - `handle` is the handle to check for uniqueness
    - `unique_across` a list of tuples, each containing a model and a field name
      for which the handle must be unique.
    """
    if unique_across is None:
        unique_across = _default_unique_across()

    is_unique = all(
        not model.objects.filter(**{field: handle}).exists()
        for model, field in unique_across
    )
    return is_unique


RANDOM_SUFFIX_LENGTH = 6


def generate_unique_handle(
    name: str,
    unique_across: T.Optional[list[T.Tuple[type, str]]] = None,
    max_attempts: int = 5,
) -> T.Optional[str]:
    """Generates a unique handle based on a name.

    If the inital handle is unique, it is returned.
    If a handle is not unique, a random suffix is appended to the handle.
    """
    base_handle = seo_tokenize(name).replace('-', '_')

    handle = base_handle
    is_unique = is_unique_handle(base_handle, unique_across=unique_across)

    if not is_unique:
        # truncate the handle to the max length
        # and leave room for a random suffix
        max_length = htk_setting('HTK_HANDLE_MAX_LENGTH')
        base_handle = base_handle[
            : max(max_length - RANDOM_SUFFIX_LENGTH, len(base_handle))
        ]
    else:
        pass

    attempts = 0
    while not is_unique:
        handle = base_handle + uuid4().hex[:RANDOM_SUFFIX_LENGTH]
        is_unique = is_unique_handle(handle)

        if attempts > max_attempts:
            rollbar.report_message('Failed to generate unique handle', 'error')
            break

    return handle
