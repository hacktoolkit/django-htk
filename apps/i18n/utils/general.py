# HTK Imports
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)


def lookup_localization(key=None, locale='en-US'):
    """Looks up a `LocalizedString` key and
    returns the value associated with that key.
    """

    LocalizedString = resolve_model_dynamically(
        htk_setting('HTK_LOCALIZED_STRING_MODEL')
    )
    try:
        localized_string = LocalizedString.objects.get(
            localizable_string__key=key,
            language_code=locale,
        ).value

    except LocalizedString.DoesNotExist:
        localized_string = f'???[{key}]-[{locale}]???'

    return localized_string
