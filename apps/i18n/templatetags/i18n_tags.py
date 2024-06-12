# Django Imports
from django import template

# HTK Imports
from htk.apps.i18n.utils.data import retrieve_all_strings


register = template.Library()


# isort: off


@register.simple_tag
def localize(key):
    '''TODO: handle this based on `by_language`
    for any language
    '''
    language_code = 'en-US'
    localized_strings = retrieve_all_strings()
    localized_string = localized_strings.get(
        key[language_code], f'???[{key}]-[{language}]???'
    )

    return localized_string
