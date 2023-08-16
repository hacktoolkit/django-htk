# Django Imports
from django import template
from django.utils.safestring import mark_safe

# HTK Imports
from htk.apps.js_urls.serializer import get_urls_as_json
from htk.utils import htk_setting


register = template.Library()


@register.simple_tag
@mark_safe
def print_js_urls():
    if not htk_setting('HTK_APPS_JS_URLS_ENABLED'):
        return ""

    js_obj = htk_setting('HTK_APPS_JS_URLS_JS_OBJECT_NAME')
    urls = get_urls_as_json()
    html = f"<script>{js_obj} = Object.assign({js_obj} || {{}}, {{ urls: {urls} }});</script>"
    return html
