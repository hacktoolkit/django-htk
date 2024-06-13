# Python Standard Library Imports
import json
import operator
import os
from functools import (
    lru_cache,
    reduce,
)

# HTK Imports
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)


@lru_cache
def look_up_supported_languages():
    """Looks up which have languages have translations.

    Returns a list of language codes.
    """
    LocalizedString = resolve_model_dynamically(
        htk_setting('HTK_LOCALIZED_STRING_MODEL')
    )
    language_codes = (
        LocalizedString.objects.values_list('language_code', flat=True)
        .order_by('language_code')
        .distinct()
    )
    return language_codes


def retrieve_all_strings(
    by_language=False, language_codes=None, namespaces=None
):
    """Returns all translated strings for every possible
    `LocalizableString` in every available language (`LocalizedString`)

    When `by_language` is `False` (default):
    - All `LocalizableString`s will be included, including those which
    have no translations available.
    - The strings will be ordered by `key`s

    The use case for including untranslated strings is to be able to send
    a batch of strings to translation vendors in bulk.

    Example structure:

    {
        'bad': {
            'en-US': 'Bad',
            'zh-CN': '壞',
        },
        'good': {
            'en-US': 'Good',
            'zh-CN': '好',
        },
    }

    When `by_language` is `True`:
    - The strings will be ordered by `language_code`
    - Additionally, if `language_codes` is supplied, only the included languages
      will be output

    Example structure:

    {
        'en-US': {
            'bad': 'Bad',
            'good': 'Good',
        },
        'zh-CN': {
            'bad': '壞',
            'good': '好',
        },
    }

    """
    if by_language:
        if language_codes is None:
            language_codes = look_up_supported_languages()

        LocalizedString = resolve_model_dynamically(
            htk_setting('HTK_LOCALIZED_STRING_MODEL')
        )

        data = {
            language_code: {
                localized_string.key_without_namespaces(
                    namespaces=[
                        namespace
                        for namespace in namespaces
                        if namespace != 'common'
                    ]
                ): localized_string.value
                for localized_string in LocalizedString.objects.filter(
                    language_code=language_code
                ).order_by('localizable_string__key')
                if (
                    len(namespaces) == 0
                    or reduce(
                        operator.or_,
                        (
                            localized_string.key.startswith(f'{namespace}.')
                            for namespace in namespaces
                        ),
                    )
                )
            }
            for language_code in language_codes
        }
    else:
        LocalizableString = resolve_model_dynamically(
            htk_setting('HTK_LOCALIZABLE_STRING_MODEL')
        )
        localizable_strings = LocalizableString.objects.order_by('key')
        data = {
            localizable_string.key: localizable_string.json_encode(
                include_key=False
            )['translations']
            for localizable_string in localizable_strings
        }

    return data


def dump_strings(file_path, indent=4, by_language=False, language_codes=None):
    data = retrieve_all_strings(
        by_language=False, language_codes=language_codes
    )

    dir_name = os.path.dirname(file_path)
    os.makedirs(dir_name, exist_ok=True)

    with open(file_path, 'w') as f:
        f.write(json.dumps(data, indent=indent))
        f.write('\n')

    num_strings = len(data)
    return num_strings


def load_strings(data, overwrite=False):
    """Load strings from `data` into `LocalizableString` and `LocalizedString`

    When `overwrite` is `True`, existing translations will be overwritten; otherwise only new translations will be added
    """
    LocalizableString = resolve_model_dynamically(
        htk_setting('HTK_LOCALIZABLE_STRING_MODEL')
    )
    num_strings = 0
    num_translations = 0

    for key, translations in data.items():
        (
            localizable_string,
            was_created,
        ) = LocalizableString.objects.get_or_create(key=key)
        num_strings += 1
        for language_code, value in translations.items():
            localized_string = localizable_string.add_translation(
                language_code, value, update=overwrite
            )
            num_translations += 1

    return num_strings, num_translations


def lookup_localization(key=None, locale='en-US'):

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
