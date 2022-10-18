# Python Standard Library Imports
import random


# isort: off


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
