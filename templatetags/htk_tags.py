import datetime
import re
import urllib

from django import template
from django.template.defaultfilters import stringfilter
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

##################################################
# Filters

# Form Utilities
@register.filter()
def field_clsname(field):
    clsname = field.field.widget.__class__.__name__
    return clsname

@register.filter(is_safe=True)
def label_with_classes(value, arg):
    attrs = {
        'class': arg,
        'className': arg,
    }
    html = value.label_tag(attrs=attrs)
    return html

@register.filter(is_safe=True)
def react_field(field):
    html = field.__str__()
    html = re.sub(r' value="(.*?)"', r' defaultValue="\g<1>"', html)
    html = re.sub(r' class="(.*?)"', r' className="\g<1>"', html)
    if field.field.widget.__class__.__name__ == 'RadioSelect':
        html = re.sub(r'checked="checked"', r'defaultChecked', html)
    html = mark_safe(html)
    return html

# Dictionary Utilities

@register.filter()
def get_item(dictionary, key):
    value = dictionary.get(key)
    return value

# String Utilities

@register.filter(is_safe=True)
def concat(value, arg):
    result = str(value) + str(arg)
    return result

@register.filter()
def zeropad(value, num_digits):
    """
    """
    padded = str(value).zfill(num_digits)
    return padded

@register.filter(is_safe=True)
def markdownify(value):
    """Converts string to markdown
    """
    import markdown
    html = markdown.markdown(value)
    return html

# Maths

@register.filter()
def int_divide(value, arg):
    return int(value) / int(arg)

@register.filter()
def float_divide(value, arg):
    return 1.0 * int(value) / int(arg)

@register.filter()
def make_range(value):
    return xrange(value)

# Formatters

@register.filter()
def currency(value):
    from decimal import Decimal
    value = Decimal(value).quantize(Decimal('0.01'))
    return value

@register.filter()
def currency_symbol(value, symbol):
    if len(value) > 0 and value[0] == '-':
        sign = '-'
        abs_value = value[1:]
    else:
        sign = ''
        abs_value = value
    result = '%s%s%s' % (sign, symbol, abs_value,)
    return result

@register.filter()
def timestamp(value):
    try:
        formatted = datetime.datetime.fromtimestamp(value)
    except AttributeError:
        formatted = ''
    return formatted

@register.filter()
def phonenumber(value, country='US'):
    """Formats a phone number for a country
    """
    import phonenumbers
    try:
        formatted = phonenumbers.format_number(phonenumbers.parse(value, country), phonenumbers.PhoneNumberFormat.NATIONAL)
    except:
        formatted = value
    return formatted

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

# Oembed

@register.filter(is_safe=True)
def oembed(value):
    from htk.lib.oembed.utils import get_oembed_html
    html = get_oembed_html(value)
    return html

# Javascript-related

@register.filter()
def jsbool(value):
    js_value = 'true' if bool(value) else 'false'
    return js_value

# Requests

@register.filter()
def http_header(value):
    """Converts Django HTTP headers to standard format
    e.g.
      HTTP_ACCEPT -> Accept
      HTTP_CACHE_CONTROL -> Cache-Control
    """
    parts = value.split('_')
    header_parts = [part.title() for part in parts[1:]]
    formatted = '-'.join(header_parts)
    return formatted

##################################################
# Tags

@register.simple_tag(takes_context=True)
def get_django_setting(context, key):
    """Retrieves a Django setting and sets it on the context dictionary
    """
    from django.conf import settings
    if hasattr(settings, key):
        value = getattr(settings, key)
        context[key] = value
    return ''

@register.simple_tag(takes_context=True)
def lesscss(context, css_file_path_base, media=None):
    """Determine whether to use LESS compilation on-the-fly or CSS files, and includes the appropriate one
    """
    media = 'media="%s" ' % media if media else ''
    values = {
        'css_rel' : context.get('css_rel', 'stylesheet'),
        'css_ext' : context.get('css_ext', 'css'),
        'css_file_path_base' : css_file_path_base,
        'media' : media,
    }
    html = '<link type="text/css" rel="%(css_rel)s" href="%(css_file_path_base)s.%(css_ext)s" %(media)s/>' % values
    html = mark_safe(html)
    return html

@register.simple_tag(takes_context=True)
def loadjs(context, js_file_path):
    """Include a JS file and append a static asset version string
    """
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
    html = mark_safe(html)
    return html

##
# ACL Tags

@register.assignment_tag(takes_context=True)
def is_editable_by_context_user(context, obj):
    user = context.get('user', None)
    if user:
        is_editable = obj.is_editable_by(user)
    else:
        is_editable = False
    return is_editable

##
# Organizations

@register.simple_tag(takes_context=True)
def is_user_organization_owner(context, organization):
    user = context.get('user', None)
    if user:
        is_owner = organization.has_owner(user)
    else:
        is_owner = False
    return is_owner

@register.simple_tag(takes_context=True)
def is_user_organization_admin(context, organization):
    user = context.get('user', None)
    if user:
        is_admin = organization.has_admin(user)
    else:
        is_admin = False
    return is_admin

@register.simple_tag(takes_context=True)
def is_user_organization_member(context, organization):
    user = context.get('user', None)
    if user:
        is_member = organization.has_member(user)
    else:
        is_member = False
    return is_member

##
# Util Tags

@register.simple_tag()
def qrcode_image_url(qr_data):
    """Returns the URL to the QR Code image of `qr_data`
    """
    if qr_data:
        from htk.lib.qrcode.utils import generate_qr_key
        from htk.utils import htk_setting
        url_name = htk_setting('HTK_QR_IMAGE_URL_NAME')
        if url_name:
            qr_params = urllib.urlencode(
                {
                    'key': generate_qr_key(qr_data),
                    'data': qr_data,
                }
            )
            image_url = '%s?%s' % (reverse(url_name), qr_params,)
        else:
            image_url = None
    else:
        image_url = None
    return image_url

@register.simple_tag()
def credit_card_icon(credit_card_brand):
    from htk.constants.icons import *
    if credit_card_brand in CREDIT_CARD_ICONS:
        credit_card_icon = CREDIT_CARD_ICONS[credit_card_brand]
    else:
        credit_card_icon = DEFAULT_CREDIT_CARD_ICON
    return credit_card_icon
