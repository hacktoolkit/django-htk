# Python Standard Library Imports
import json
import re
from urllib.parse import urljoin

# Django Imports
from django.urls import get_resolver
from django.urls.resolvers import (
    RegexPattern,
    RoutePattern,
    URLPattern,
    URLResolver,
)

# HTK Imports
from htk.utils import htk_setting
from htk.utils.strings import (
    replace,
    snake_case_to_lower_camel_case,
)


URL_ARG_RE = re.compile(r'(\(.*?\))')
URL_KWARG_RE = re.compile(r'(\(\?P\<(.*?)\>.*?\))')
URL_OPTIONAL_CHAR_RE = re.compile(r'(?:\w|/)(?:\?|\*)')
URL_OPTIONAL_GROUP_RE = re.compile(r'\(\?\:.*\)(?:\?|\*)')
URL_PATH_RE = re.compile(r'(\<.*?\>)')


def build_routes(resolver=None, as_json=False):
    resolver = resolver or get_resolver()
    routes = dict(_parse_resolver(resolver))

    # Convert `snake_case` dict keys to `camelCase`
    if htk_setting('HTK_JS_ROUTER_USE_CAMEL_CASE_URL_NAMES'):
        routes = {
            snake_case_to_lower_camel_case(key): value
            for key, value in routes.items()
        }

    if as_json:
        routes = json.dumps(routes)
    return routes


def _parse_resolver(
    resolver, namespace=None, url_prefix=None, include_all=False
):
    """Parse Resolver

    Traverses URL patterns recursively starting from the root URL pattern
    defined in `settings.URL_CONF`. Recursive is required since URL paths
    are being included with `django.urls.include`.

    Supports namespaces and nested namespaces.
    """
    defined_url_names = htk_setting('HTK_JS_ROUTES_URL_NAMES')

    current_namespace = (
        f'{namespace}:{resolver.namespace}' if namespace else resolver.namespace
    )
    include_all = include_all or (current_namespace in defined_url_names)

    urls = []
    for url_pattern in resolver.url_patterns:
        if isinstance(url_pattern, URLResolver):
            new_url_prefix = _prepare_url_part(url_pattern)
            new_url_prefix = (
                '/' + new_url_prefix
                if url_prefix is None
                else urljoin(url_prefix or '/', new_url_prefix)
            )

            urls += _parse_resolver(
                url_pattern,
                namespace=current_namespace,
                url_prefix=new_url_prefix,
                include_all=include_all,
            )
        elif isinstance(url_pattern, URLPattern) and url_pattern.name:
            url_name = (
                f'{current_namespace}:{url_pattern.name}'
                if current_namespace
                else url_pattern.name
            )
            if url_name in defined_url_names or include_all:
                full_url = _prepare_url_part(url_pattern)
                urls.append((url_name, urljoin(url_prefix or '/', full_url)))

    return urls


def _prepare_url_part(url_pattern):
    """Prepare URL Part

    Prepares URL path with changing dynamic parts to a placeholder can be set by
    HTK_JS_ROUTES_DYNAMIC_PART_PLACEHOLDER setting. Default is `{0}`

    - Converts `/some_path/(?P<id>\d)` to `/some_path/{0}`
    - Removes optional parts like `(\d+)?`

    It supports:
      - Named regexp paths like `(?P<id>\d+)`
      - Unnamed regexp paths like `(\d+)`
      - Django paths like `<id:int>`
    """
    url = ""
    placeholder = htk_setting('HTK_JS_ROUTES_DYNAMIC_PART_PLACEHOLDER')

    if hasattr(
        url_pattern, 'regex'
    ):  # pragma: no cover, NOTE: Django < 2.0 compatibility
        url = url_pattern.regex.pattern
    elif isinstance(url_pattern.pattern, RegexPattern):
        url = url_pattern.pattern._regex
    elif isinstance(url_pattern.pattern, RoutePattern):
        url = url_pattern.pattern._route

    final_url = replace(url, [('^', ''), ('$', '')])

    # Removes optional groups from the URL pattern.
    optional_group_matches = URL_OPTIONAL_GROUP_RE.findall(final_url)
    final_url = (
        replace(final_url, [(el, "") for el in optional_group_matches])
        if optional_group_matches
        else final_url
    )

    # Removes optional characters from the URL pattern.
    optional_char_matches = URL_OPTIONAL_CHAR_RE.findall(final_url)
    final_url = (
        replace(final_url, [(el, "") for el in optional_char_matches])
        if optional_char_matches
        else final_url
    )

    # Identifies named URL arguments inside the URL pattern.
    kwarg_matches = URL_KWARG_RE.findall(final_url)
    final_url = (
        replace(final_url, [(el[0], placeholder) for el in kwarg_matches])
        if kwarg_matches
        else final_url
    )

    # Identifies unnamed URL arguments inside the URL pattern.
    args_matches = URL_ARG_RE.findall(final_url)
    final_url = (
        replace(final_url, [(el, placeholder) for el in args_matches])
        if args_matches
        else final_url
    )

    # Identifies path expression and associated converters inside the URL pattern.
    path_matches = URL_PATH_RE.findall(final_url)
    final_url = (
        replace(final_url, [(el, placeholder) for el in path_matches])
        if (path_matches and not (kwarg_matches or args_matches))
        else final_url
    )

    return final_url
