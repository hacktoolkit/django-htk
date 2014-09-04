from django.template.base import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter(is_safe=True)
def concat(value, arg):
    result = str(value) + str(arg)
    return result

@register.filter()
def phonenumber(value, country='US'):
    """Formats a phone number for a country
    """
    import phonenumbers
    formatted = phonenumbers.format_number(phonenumbers.parse(value, country), phonenumbers.PhoneNumberFormat.NATIONAL)
    return formatted

@register.filter()
def zeropad(value, num_digits):
    """
    """
    padded = str(value).zfill(num_digits)
    return padded

@register.filter(is_safe=True)
def obfuscate(value):
    """Obfuscates a string
    """
    from htk.utils.obfuscate import html_obfuscate_string
    result = html_obfuscate_string(value)
    return result

@register.filter(is_safe=True)
def obfuscate_mailto(value, text=False):
    """Obfuscates a mailto link
    """
    from htk.utils.obfuscate import html_obfuscate_string
    email = html_obfuscate_string(value)

    if text:
        link_text = text
    else:
        link_text = email

    result = '<a href="%s%s">%s</a>' % (
        html_obfuscate_string('mailto:'),
        email,
        link_text,
    )
    return result

@register.simple_tag(takes_context=True)
def lesscss(context, css_file_path_base, media=None):
    media = 'media="%s" ' % media if media else ''
    values = {
        'css_rel' : context.get('css_rel', 'stylesheet'),
        'css_ext' : context.get('css_ext', 'css'),
        'css_file_path_base' : css_file_path_base,
        'media' : media,
    }
    html = '<link type="text/css" rel="%(css_rel)s" href="%(css_file_path_base)s.%(css_ext)s" %(media)s/>' % values
    return html

@register.simple_tag(takes_context=True)
def loadjs(context, js_file_path):
    asset_version = context.get('asset_version')
    if asset_version:
        asset_version_str = '?v=%s' % asset_version
    else:
        asset_version_str = ''
    values = {
        'js_file_path' : js_file_path,
        'asset_version_str' : asset_version_str,
    }
    html = '<script type="text/javascript" src="%(js_file_path)s%(asset_version_str)s"></script>' % values
    return html
