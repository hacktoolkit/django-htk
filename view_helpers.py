import re
from socket import gethostname

from django.conf import settings
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import loader
from django.template import TemplateDoesNotExist

from htk.cachekeys import StaticAssetVersionCache
from htk.utils import utcnow

def render_to_response_custom(template_name, data=None, template_prefix=''):
    """Wrapper function for django.shortcuts.render_to_response

    Puts additional information needed onto the context dictionary
    """
    if data is None:
        data = {}

    # pre-render
    data['javascripts'] = get_javascripts(template_name, template_prefix=template_prefix)
    _build_meta_content(data)

    # render
    response = render_to_response(template_name, data)
    return response

def get_javascripts(template_name, template_prefix=''):
    """Get a list of JavaScript includes for the specified `template_name`

    HTML templates need to know about a list of JavaScript files to include beforehand.
    This is so that we can place the include statement as close to the closing body tag as possible, to prevent possible DOM errors or page loading race conditions.
    """
    javascripts = []

    admin_template_match = re.match('%sadmintools/(.*)' % template_prefix, template_name)
    if admin_template_match:
        js_fragment_filename = '%sadmintools/fragments/js/%s' % (template_prefix, admin_template_match.group(1),)
    else:
        template_prefix_match = re.match('%s(.*)' % template_prefix, template_name)
        if template_prefix_match:
            js_fragment_filename = '%sfragments/js/%s' % (template_prefix, template_prefix_match.group(1),)
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
        asset_version = now.strftime('%Y%m%d%H')
    return asset_version

def wrap_data(request, data=None):
    """Puts commonly used values into the template context dictionary, `data`
    """
    if data is None:
        data = {}

    # CSRF Token
    data.update(csrf(request))

    ##
    # meta, server, request info
    path = request.path
    host = request.get_host()
    is_secure = request.is_secure()
    full_uri = '%s://%s%s' % ('http' + ('s' if is_secure else ''), host, path,)
    data['request'] = {
        'request' : request,
        'is_secure' : is_secure,
        'host' : host,
        'path' : path,
        'full_uri' : full_uri,
    }
    data['server'] = {
        'hostname' : gethostname(),
    }

    data['meta'] = {
        'title' : {
            'content' : '',
            'inverted' : [],
            'join_value' : ' | ',
        },
        'description' : {
            'content' : '',
            'inverted' : [],
            'join_value' : ' ',
         },
        'keywords' : {
            'content' : '',
            'inverted' : [],
            'join_value' : ',',
         },
    }

    ##
    # Rollbar
    data['rollbar'] = {
        'env' : settings.ROLLBAR_ENV,
        'tokens' : {
            'post_client_item' : settings.ROLLBAR_TOKEN_POST_CLIENT_ITEM,
        },
    }

    # LESS http://lesscss.org/#usage
    asset_version = get_asset_version()
    useless = settings.ENV_DEV and request.GET.get('useless', False)
    data['css_rel'] = 'stylesheet/less' if useless else 'stylesheet'
    data['css_ext'] = 'less' if useless else 'css?v=%s' % asset_version
    data['asset_version'] = asset_version

    ##
    # user
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    data['user'] = user

    ##
    # errors
    data['errors'] = []

    return data

def _build_meta_content(data):
    """Build page title and META description and keywords before rendering
    """
    if type(data.get('meta')) == dict:
        for meta_type, config in data['meta'].items():
            inverted_content = config['inverted']
            config['content'] = config['join_value'].join(inverted_content[::-1])

def _set_meta_content(meta_type, value, data):
    if hasattr(value, '__iter__'):
        values_list = value
    else:
        values_list = [value,]
    data['meta'][meta_type]['inverted'] = values_list

def _add_meta_content(meta_type, value, data):
    if hasattr(value, '__iter__'):
        values_list = value
    else:
        values_list = [value,]
    data['meta'][meta_type]['inverted'] += values_list

def set_page_title(title, data):
    """Sets the page title

    Overwrites any previously set or added title
    """
    _set_meta_content('title', title, data)

def add_page_title(title, data):
    """Adds an additioanl phrase to page title
    """
    _add_meta_content('title', title, data)

def set_meta_description(description, data):
    """Sets the META description

    Overwrites any previously set or added META description
    """
    _set_meta_content('description', description, data)

def add_meta_description(description, data):
    """Adds an additional sentence or phrase to META description
    """
    _add_meta_content('description', description, data)

def set_meta_keywords(keywords, data):
    """Sets the META keywords

    Overwrites any previously set or added META keywords
    """
    _set_meta_content('keywords', keywords, data)

def add_meta_keywords(keywords, data):
    """Adds an additional keyword to META keywords

    `keywords` must be a list in order of least significant to most significant terms
    """
    _add_meta_content('keywords', keywords, data)
