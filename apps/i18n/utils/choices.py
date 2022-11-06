# HTK Imports
from htk.utils import htk_setting


def get_language_code_choices():
    language_codes = htk_setting('HTK_LOCALIZABLE_STRING_LANGUAGE_CODES')
    choices = [
        (
            language_code,
            language_code,
        )
        for language_code in language_codes
    ]
    return choices
