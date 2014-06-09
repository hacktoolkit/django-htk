import re
from socket import gethostname

from django.conf import settings
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import loader
from django.template import TemplateDoesNotExist

from htk.cachekeys import StaticAssetVersionCache
from htk.utils import htk_setting
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
    url_name = request.resolver_match.url_name
    host = request.get_host()
    is_secure = request.is_secure()
    full_uri = '%s://%s%s' % ('http' + ('s' if is_secure else ''), host, path,)
    data['request'] = {
        'request' : request,
        'is_secure' : is_secure,
        'host' : host,
        'path' : path,
        'url_name' : url_name,
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
        add_static_page_title(data)
        add_static_meta_description(data)
        for meta_type, config in data['meta'].items():
            inverted_content = config['inverted']
            config['content'] = config['join_value'].join(inverted_content[::-1])

def _set_meta_content(meta_type, value, data):
    meta = data.get('meta', {}).get(meta_type)
    if meta:
        if hasattr(value, '__iter__'):
            values_list = value
        else:
            values_list = [value,]
        meta['inverted'] = values_list
    else:
        pass

def _add_meta_content(meta_type, value, data):
    meta = data.get('meta', {}).get(meta_type)
    if meta:
        if hasattr(value, '__iter__'):
            values_list = value
        else:
            values_list = [value,]
        meta['inverted'] += values_list
    else:
        pass

def add_static_page_title(data):
    """Tries to add a static page title
    """
    request = data.get('request', {}).get('request')
    if request:
        url_name = request.resolver_match.url_name
        default_static_page_titles = data.get('meta', {}).get('title', {}).get('static_page_titles', None)
        static_page_titles = htk_setting('HTK_STATIC_PAGE_TITLES', default=default_static_page_titles)
        if url_name in static_page_titles:
            title = static_page_titles[url_name]
            add_page_title(title, data)
        else:
            pass
    else:
        pass

def set_page_title(title, data):
    """Sets the page title

    Overwrites any previously set or added title
    """
    _set_meta_content('title', title, data)

def add_page_title(title, data):
    """Adds an additional phrase to page title
    """
    _add_meta_content('title', title, data)

def add_static_meta_description(data):
    """Tries to add a static meta description
    """
    request = data.get('request', {}).get('request')
    if request:
        url_name = request.resolver_match.url_name
        default_static_meta_descriptions = data.get('meta', {}).get('description', {}).get('static_meta_descriptions', None)
        static_meta_descriptions = htk_setting('HTK_STATIC_META_DESCRIPTIONS', default=default_static_meta_descriptions)
        if url_name in static_meta_descriptions:
            description = static_meta_descriptions[url_name]
            add_meta_description(description, data)
        else:
            pass
    else:
        pass

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
