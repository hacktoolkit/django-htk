# Python Standard Library Imports
import re

# Django Imports
from django import template


register = template.Library()


@register.filter()
def pinyin(value):
    import pinyin
    result = pinyin.get(value, delimiter=' ')

    patterns_replacements = (
        (r'\{.*( ).*\}', ''),
        (r' +', ' ',),
        (r'\( ', '(',),
        (r' \) ', ')'),
        (r'\[ ', '[',),
        (r' \] ', ']'),
    )
    for pattern, replacement in patterns_replacements:
        result = re.sub(pattern, replacement, result)

    return result


@register.filter()
def chinese_english_translate(value):
    import pinyin.cedict

    translations = []
    for line in value.split('\n'):
        for word in line:
            translation = pinyin.cedict.translate_word(word)
            if translation:
                translations.append(translation[0])
        translations.append('\n')
    result = ' '.join(translations)
    return result
