# Python Standard Library Imports
import base64
import datetime
import json
import re

# Third Party (PyPI) Imports
import six.moves.urllib as urllib

# Django Imports
from django import template
from django.template import (
    Context,
    Template,
)
from django.template.defaultfilters import stringfilter
from django.urls import reverse
from django.utils.safestring import (
    SafeText,
    mark_safe,
)

# HTK Imports
from htk.compat import (
    b64decode,
    b64encode,
)


register = template.Library()


# isort: off


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
    """ """
    padded = str(value).zfill(num_digits)
    return padded


@register.filter(is_safe=True)
def markdownify(value):
    """Converts Markdown string to HTML"""
    import markdown

    html = markdown.markdown(value)
    return html


@register.filter()
def atob(value):
    """Base64 decode
    ASCII to Binary
    """
    value = b64decode(value)
    return value


@register.filter()
def btoa(value):
    """Base64 encode
    Binary to ASCII
    """
    if type(value) in (str, SafeText):
        value = value.encode('utf-8')

    value = b64encode(value)

    return value


# Maths


@register.filter()
def int_divide(value, arg):
    return int(value) / int(arg)


@register.filter()
def float_divide(value, arg):
    return 1.0 * int(value) / int(arg)


@register.filter()
def make_range(value):
    return range(value)


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
    result = '%s%s%s' % (
        sign,
        symbol,
        abs_value,
    )
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
    """Formats a phone number for a country"""
    from htk.utils.text import pretty

    formatted = pretty.phonenumber(value, country=country)
    return formatted


@register.filter(is_safe=True)
def obfuscate(value):
    """Obfuscates a string"""
    from htk.utils.obfuscate import html_obfuscate_string

    result = html_obfuscate_string(value)
    return result


@register.filter(is_safe=True)
def obfuscate_mailto(value, text=False):
    """Obfuscates a mailto link"""
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
def oembed(value, autoplay=False):
    from htk.lib.oembed.utils import get_oembed_html

    html = get_oembed_html(value, autoplay=autoplay)
    html = mark_safe(html)
    return html


# Javascript-related


@register.filter()
def jsbool(value):
    js_value = 'true' if bool(value) else 'false'
    return js_value


@register.filter()
def jsondumps(value, indent=None):
    js_value = mark_safe(json.dumps(value, indent=indent))
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
    """Retrieves a Django setting and sets it on the context dictionary"""
    from django.conf import settings

    if hasattr(settings, key):
        value = getattr(settings, key)
        context[key] = value
    return ''


@register.simple_tag()
def htk_setting(key):
    from htk.utils import htk_setting as _htk_setting

    value = _htk_setting(key)
    return value


@register.simple_tag(takes_context=True)
def render_string(context, template_string):
    """Renders a Django template string with the given context

    Useful for rendering dynamic template strings in a template
    """
    t = Template(template_string)
    return t.render(Context(context))


@register.simple_tag()
def get_request_duration():
    from htk.middleware.classes import RequestTimerMiddleware

    timer = RequestTimerMiddleware.get_current_timer()
    if timer:
        duration = timer.duration()
    else:
        # TODO: fix get_current_timer()
        duration = 0
    return duration


##
# Load Assets


@register.simple_tag(takes_context=True)
def lesscss(context, css_file_path_base, media=None):
    """Determine whether to use LESS compilation on-the-fly or CSS files, and includes the appropriate one"""
    media = 'media="%s" ' % media if media else ''
    values = {
        'css_rel': context.get('css_rel', 'stylesheet'),
        'css_ext': context.get('css_ext', 'css'),
        'css_file_path_base': css_file_path_base,
        'media': media,
    }
    html = (
        '<link type="text/css" rel="%(css_rel)s" href="%(css_file_path_base)s.%(css_ext)s" %(media)s/>'
        % values
    )
    html = mark_safe(html)
    return html


@register.simple_tag(takes_context=True)
def loadjs(context, js_file_path, jsx=False):
    """Include a JS file and append a static asset version string"""
    asset_version = context.get('asset_version')
    if asset_version:
        asset_version_str = '?v=%s' % asset_version
    else:
        asset_version_str = ''
    values = {
        'script_type': 'text/babel' if jsx else 'text/javascript',
        'js_file_path': js_file_path,
        'asset_version_str': asset_version_str,
    }
    html = (
        '<script type="%(script_type)s" src="%(js_file_path)s%(asset_version_str)s"></script>'
        % values
    )
    html = mark_safe(html)
    return html


@register.simple_tag(takes_context=True)
def loadjsx(context, js_file_path):
    html = loadjs(context, js_file_path, jsx=True)
    return html


##
# Feature Flags


@register.simple_tag()
def is_feature_enabled(feature_name):
    from htk.apps.features.utils import (
        is_feature_enabled as _is_feature_enabled,
    )

    is_enabled = _is_feature_enabled(feature_name)
    return is_enabled


##
# ACL Tags


@register.simple_tag(takes_context=True)
def is_editable_by_context_user(context, obj):
    user = context.get('user', None)
    if user:
        is_editable = obj.is_editable_by(user)
    else:
        is_editable = False
    return is_editable


@register.simple_tag(takes_context=True)
def has_permission(context, permission_key):
    request = context.get('request', {}).get('request', None)
    user = request.user
    if request and user.is_authenticated:
        has_permission = user.has_perm(permission_key)
    else:
        has_permission = False

    return has_permission


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
# Geolocations


@register.simple_tag()
def distance_from(obj, lat, lng, unit='mile'):
    from htk.apps.geolocations.enums import DistanceUnit
    from htk.apps.geolocations.models import AbstractGeolocation

    if not isinstance(obj, AbstractGeolocation) and not hasattr(
        obj, 'distance_from'
    ):
        raise Exception(
            'Not a Geolocation object or does not have a distance_from method'
        )

    distance_unit_map = {
        'meter': DistanceUnit.METER,
        'kilometer': DistanceUnit.KILOMETER,
        'feet': DistanceUnit.FEET,
        'mile': DistanceUnit.MILE,
    }

    distance_unit = distance_unit_map.get(unit)

    if distance_unit is None:
        raise Exception('Unknown distance unit: %s' % unit)

    distance = obj.distance_from(lat, lng, distance_unit=distance_unit)

    return distance


##
# Util Tags


@register.simple_tag()
def qrcode_image_url(qr_data):
    """Returns the URL to the QR Code image of `qr_data`"""
    if qr_data:
        from htk.lib.qrcode.utils import generate_qr_key
        from htk.utils import htk_setting

        url_name = htk_setting('HTK_QR_IMAGE_URL_NAME')
        if url_name:
            qr_params = urllib.parse.urlencode(
                {
                    'key': generate_qr_key(qr_data),
                    'data': qr_data,
                }
            )
            image_url = '%s?%s' % (
                reverse(url_name),
                qr_params,
            )
        else:
            image_url = None
    else:
        image_url = None
    return image_url


@register.simple_tag()
def credit_card_icon(credit_card_brand):
    from htk.constants.icons import CREDIT_CARD_ICONS
    from htk.constants.icons import DEFAULT_CREDIT_CARD_ICON

    if credit_card_brand in CREDIT_CARD_ICONS:
        credit_card_icon = CREDIT_CARD_ICONS[credit_card_brand]
    else:
        credit_card_icon = DEFAULT_CREDIT_CARD_ICON
    return credit_card_icon


@register.simple_tag()
@mark_safe
def print_js_routes():
    from htk.utils.js_route_serializer import build_routes

    urls = build_routes(as_json=True)
    return urls
