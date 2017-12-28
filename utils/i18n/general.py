import random

def get_random_greeting():
    from htk.constants.i18n.greetings import I18N_GREETINGS
    lang = random.choice(I18N_GREETINGS.keys())
    greeting = random.choice(I18N_GREETINGS[lang])
    return greeting

