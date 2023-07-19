# Python Standard Library Imports
import random


# isort: off


def get_country_choices(
    ordering=(
        'US',
        'CA',
    )
):
    """Builds a list of country choices

    `ordering` - A custom list of country codes which should appear first

    Returns a list of pairs: (ISO 3166 country code, country name)
    """
    from htk.constants.i18n.countries import COUNTRIES_EN_NAMES_MAP

    country_codes = [country_code for country_code in ordering] + [
        country_code
        for country_code in COUNTRIES_EN_NAMES_MAP.keys()
        if country_code not in ordering
    ]
    choices = [
        (
            country_code,
            COUNTRIES_EN_NAMES_MAP[country_code],
        )
        for country_code in country_codes
    ]
    return choices


def get_language_name(language_code):
    from htk.constants.i18n import LANGUAGE_NAMES_MAP

    language_name = LANGUAGE_NAMES_MAP.get(language_code)
    return language_name


def get_currency_symbol(currency_code):
    from htk.constants.i18n.currency import CURRENCY_CODE_TO_SYMBOLS_MAP

    curency_symbol = CURRENCY_CODE_TO_SYMBOLS_MAP.get(currency_code)
    return curency_symbol


def get_random_greeting():
    from htk.constants.i18n.greetings import I18N_GREETINGS

    lang = random.choice(list(I18N_GREETINGS.keys()))
    greeting = random.choice(I18N_GREETINGS[lang])
    return greeting
