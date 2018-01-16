import copy
import re
import rollbar
from socket import gethostname

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import loader
from django.template import TemplateDoesNotExist
from django.template.context_processors import csrf
from django.urls import reverse

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
    _build_breadcrumbs(data)

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
    from htk.utils.request import get_request_metadata
    data['request'] = get_request_metadata(request)
    data['server'] = {
        'hostname' : gethostname(),
    }

    data['site_name'] = htk_setting('HTK_SITE_NAME')

    data['meta'] = {
        'title' : {
            'content' : '',
            'inverted' : [],
            'join_value' : ' | ',
            'static_values' : {},
        },
        'breadcrumbs' : {
            'url_names_to_breadcrumbs' : {},
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

    data['privacy_url_name'] = 'privacy'
    data['robots_url_name'] = 'robots'

    ##
    # Rollbar
    data['rollbar'] = {
        'env' : settings.ROLLBAR_ENV,
        'branch' : settings.ROLLBAR.get('branch', 'master'),
        'tokens' : {
            'post_client_item' : settings.ROLLBAR_TOKEN_POST_CLIENT_ITEM,
        },
        'host_blacklist' : settings.ROLLBAR.get('host_blacklist', None),
        'host_whitelist' : settings.ROLLBAR.get('host_whitelist', None),
        'ignored_messages' : settings.ROLLBAR.get('ignored_messages', None),
        'ignored_messages_regexes' : settings.ROLLBAR.get('ignored_messages_regexes', None),
        'ignored_uncaught_exception_classes' : settings.ROLLBAR.get('ignored_uncaught_exception_classes', None),
    }

    ##
    # LESS http://lesscss.org/#usage
    asset_version = get_asset_version()
    css_ext = '%s?v=%s' % (htk_setting('HTK_CSS_EXTENSION'), asset_version,)
    useless = settings.ENV_DEV and request.GET.get('useless', False)
    data['css_rel'] = 'stylesheet/less' if useless else 'stylesheet'
    data['css_ext'] = 'less' if useless else css_ext
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

def update_top_level_constants(context):
    """Updates top-level key-values in `context` from `context['constants']`
    """
    constants = context.get('constants', {})
    if constants:
        keys = [
            'privacy_url_name',
            'robots_url_name',
        ]
        for key in keys:
            if key in constants:
                context[key] = constants[key]

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

def _build_meta_content(data):
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
                config['value'] = inverted_content[-1] if len(inverted_content) else ''
            except:
                request = data.get('request', {}).get('request')
                rollbar.report_exc_info(request=request)

def _build_breadcrumbs(data):
    if data.get('has_dynamic_breadcrumbs', False):
        request = data.get('request', {}).get('request')
        if request:
            resolver_matches_chain = get_resolver_matches_chain(request)
            url_names_to_breadcrumbs = data.get('meta', {}).get('breadcrumbs', {}).get('url_names_to_breadcrumbs', {})
            inverted_breadcrumbs = []
            for path, resolver_match in resolver_matches_chain:
                title = url_names_to_breadcrumbs.get(resolver_match.url_name, None)
                if title:
                    inverted_breadcrumbs.append({
                        'url' : path,
                        'title' : title,
                    })

            data['breadcrumbs'] = inverted_breadcrumbs[::-1]

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

def add_page_title(title, data=None, url_name=None):
    """Adds an additional phrase to page title

    If `url_name` is specified, also associates `title` with `url_name` for breadcrumbs lookup
    """
    _update_meta_content('title', title, update_type='add', data=data)
    if url_name and data:
        add_breadcrumb_mapping(url_name, title, data)

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

def add_breadcrumb_mapping(url_name, title, data):
    url_names_to_breadcrumbs = data.get('meta', {}).get('breadcrumbs', {}).get('url_names_to_breadcrumbs', {})
    url_names_to_breadcrumbs[url_name] = title

def get_resolver_matches_chain(request, data=None):
    """Walk the current request URL path up to the top, attempting to resolve along the way
    """
    from django.urls import Resolver404
    from django.urls import resolve
    resolver_matches_chain = []
    path = request.path
    resolver_matches_chain.append((path, request.resolver_match,))
    while path:
        try:
            path = path[:path.rindex('/')]
            resolver_match = resolve(path)
            resolver_matches_chain.append((path, resolver_match))
        except Resolver404:
            # could not resolve without '/'
            path_with_slash = path + '/'
            if request.path != path_with_slash:
                try:
                    resolver_match = resolve(path_with_slash)
                    resolver_matches_chain.append((path_with_slash, resolver_match))
                except Resolver404:
                    pass
        except ValueError:
            # '/' substring not found
            break
    return resolver_matches_chain

def generate_nav_links(request, nav_links_cfg):
    """Generate navigation menu links from a configuration dictionary

    Allows for nested submenus
    """
    url_name = request.resolver_match.url_name
    nav_links = []
    for link_cfg in nav_links_cfg:
        nav_link = copy.copy(link_cfg)
        submenu = link_cfg.get('submenu', None)
        cfg_url_name = link_cfg.get('url_name', None)
        if cfg_url_name:
            nav_link['uri'] = reverse(cfg_url_name)
        else:
            pass
        selected = url_name == cfg_url_name
        nav_link['selected'] = selected
        if submenu:
            nav_link['submenu'] = generate_nav_links(request, submenu)
        else:
            pass
        nav_links.append(nav_link)
    return nav_links
