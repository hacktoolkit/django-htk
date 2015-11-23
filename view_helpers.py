import re
import rollbar
from socket import gethostname

from django.conf import settings
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import loader
from django.template import TemplateDoesNotExist

from htk.cachekeys import StaticAssetVersionCache
from htk.session_keys import *
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
            'static_values' : {},
        },
        'description' : {
            'content' : '',
            'inverted' : [],
            'join_value' : ' ',
            'static_values' : {},
         },
        'keywords' : {
            'content' : '',
            'inverted' : [],
            'join_value' : ',',
            'static_values' : {},
        },
        'site_verifications' : {},
    }

    ##
    # Rollbar
    data['rollbar'] = {
        'env' : settings.ROLLBAR_ENV,
        'branch' : settings.ROLLBAR.get('branch', 'master'),
        'tokens' : {
            'post_client_item' : settings.ROLLBAR_TOKEN_POST_CLIENT_ITEM,
        },
    }

    ##
    # LESS http://lesscss.org/#usage
    asset_version = get_asset_version()
    useless = settings.ENV_DEV and request.GET.get('useless', False)
    data['css_rel'] = 'stylesheet/less' if useless else 'stylesheet'
    data['css_ext'] = 'less' if useless else 'css?v=%s' % asset_version
    data['asset_version'] = asset_version

    ##
    # Current Environment
    data['ENV_DEV'] = settings.ENV_DEV
    data['ENV_PROD'] = settings.ENV_PROD

    ##
    # Javascript reloader
    _javascript_reloader(request, data)

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

def _javascript_reloader(request, data):
    """Since pages may depend on JavaScript to function properly,
    we may receive requests from front-end to force-reload

    Need to keep track of reload attempts to avoid infinite reloads
    """
    if request.GET.get(YUI_RELOAD, None):
        request.session[YUI_RELOAD_ATTEMPTS] = request.session.get(YUI_RELOAD_ATTEMPTS, 0) + 1
    else:
        request.session[YUI_RELOAD_ATTEMPTS] = 0
    data['JS_RELOADS'] = {
        'yui' : request.session[YUI_RELOAD_ATTEMPTS],
    }

def _build_meta_content(data=None):
    """Build page title and META description and keywords before rendering
    """
    if data is None:
        data = {}
    meta = data.get('meta', {})
    if meta and type(meta) == dict:
        for meta_type, config in meta.items():
            _add_static_meta_content(meta_type, data)
            try:
                inverted_content = config.get('inverted', [])
                config['content'] = config.get('join_value', '').join(inverted_content[::-1])
                config['value'] = inverted_content[-1]
            except:
                request = data.get('request', {}).get('request')
                rollbar.report_exc_info(request=request)

def _update_meta_content(meta_type, value, update_type='set', data=None):
    if data is None:
        data = {}
    meta = data.get('meta', {}).get(meta_type)
    if meta:
        if hasattr(value, '__iter__'):
            values_list = value
        else:
            values_list = [value,]
        if update_type == 'set':
            meta['inverted'] = values_list
        elif update_type == 'add':
            meta['inverted'] += values_list
        else:
            # unknown update_type
            pass
    else:
        pass

def _add_static_meta_content(meta_type, data=None):
    """Tries to add static meta content

    Currently handles:
    - page titles
    - meta description

    Could handle meta keywords as well, but doesn't make sense for those to be static?
    """
    meta = data.get('meta', {}).get(meta_type, {})
    default_static_values = meta.get('static_values', None)
    static_values = htk_setting('HTK_STATIC_META_%s_VALUES' % meta_type.upper(), default=default_static_values)
    request = data.get('request', {}).get('request')
    if meta and static_values and request:
        url_name = request.resolver_match.url_name
        path = request.path
        static_value = static_values.get(url_name, static_values.get(path, None))
        if static_value:
            _update_meta_content(meta_type, static_value, update_type='add', data=data)
        else:
            pass
    else:
        pass

def set_page_title(title, data=None):
    """Sets the page title

    Overwrites any previously set or added title
    """
    _update_meta_content('title', title, update_type='set', data=data)

def add_page_title(title, data=None):
    """Adds an additional phrase to page title
    """
    _update_meta_content('title', title, update_type='add', data=data)

def set_meta_description(description, data=None):
    """Sets the META description

    Overwrites any previously set or added META description
    """
    _update_meta_content('description', description, update_type='set', data=data)

def add_meta_description(description, data=None):
    """Adds an additional sentence or phrase to META description
    """
    _update_meta_content('description', description, update_type='add', data=data)

def set_meta_keywords(keywords, data=None):
    """Sets the META keywords

    Overwrites any previously set or added META keywords
    """
    _update_meta_content('keywords', keywords, update_type='set', data=data)

def add_meta_keywords(keywords, data=None):
    """Adds an additional keyword to META keywords

    `keywords` must be a list in order of least significant to most significant terms
    """
    _update_meta_content('keywords', keywords, update_type='add', data=data)

def generate_nav_links(request, nav_links_cfg):
    """Generate navigation menu links from a configuration dictionary

    Allows for nested submenus
    """
    url_name = request.resolver_match.url_name
    nav_links = []
    for link_cfg in nav_links_cfg:
        text = link_cfg['text']
        submenu = link_cfg.get('submenu', None)
        cfg_url_name = link_cfg.get('url_name', None)
        if cfg_url_name:
            uri = reverse(cfg_url_name)
        else:
            uri = link_cfg.get('uri')
        selected = url_name == cfg_url_name
        nav_link = {
            'text' : text,
            'uri' : uri,
            'selected' : selected,
        }
        if submenu:
            nav_link['submenu'] = generate_nav_links(request, submenu)
        else:
            pass
        nav_links.append(nav_link)
    return nav_links
