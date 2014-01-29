import re

from django.shortcuts import render_to_response
from django.template import loader
from django.template import TemplateDoesNotExist

from htk.cachekeys import StaticAssetVersionCache
from htk.utils import utcnow

def render_to_response_custom(template_name, data=None):
    """Wrapper function for django.shortcuts.render_to_response

    Puts additional information needed onto the context dictionary
    """
    if data is None:
        data = {}

    data['javascripts'] = get_javascripts(template_name)
    response = render_to_response(template_name, data)
    return response

def get_javascripts(template_name):
    """Get a list of JavaScript includes for the specified `template_name`

    HTML templates need to know about a list of JavaScript files to include beforehand.
    This is so that we can place the include statement as close to the closing body tag as possible, to prevent possible DOM errors or page loading race conditions.
    """
    javascripts = []

    admin_template_match = re.match('([a-z]*admin)/(.*)', template_name)
    if admin_template_match:
        js_fragment_filename = '%s/fragments/js/%s' % (admin_template_match.group(1), admin_template_match.group(2),)
    else:
        js_fragment_filename = 'fragments/js/%s' % template_name
    #if template_name in SOME_DICTIONARY_MAPPING_JAVASCRIPTS:
    #    javascript.append(SOME_DICTIONARY_MAPPING_JAVASCR

    # check to see if there exists the default javascript for this template
    try:
        t = loader.get_template(js_fragment_filename)
    except TemplateDoesNotExist:
        t = None
    if t is not None:
        javascripts.append(js_fragment_filename)

    return javascripts

def get_asset_version():
    """Get asset_version from cache
    This value is updated whenever we deploy. See fab_helpers.py

    If not available from cache, default value is current date.
    """
    c = StaticAssetVersionCache()
    asset_version = c.get()
    if asset_version is None:
        now = utcnow()
        asset_version = now.strftime('%Y%m%d')
    return asset_version
