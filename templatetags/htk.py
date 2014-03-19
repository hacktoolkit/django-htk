from django.template.base import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter(is_safe=True)
def concat(value, arg):
    result = str(value) + str(arg)
    return result
