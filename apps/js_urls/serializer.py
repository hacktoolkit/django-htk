# Python Standard Library Imports
import json
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
from htk.apps.js_urls.constants.regexp import (
    URL_ARG_RE,
    URL_KWARG_RE,
    URL_OPTIONAL_CHAR_RE,
    URL_OPTIONAL_GROUP_RE,
    URL_PATH_RE,
)
from htk.apps.js_urls.utils import replace
from htk.utils import htk_setting


def get_urls_as_dict(resolver=None):
    resolver = resolver or get_resolver()
    return dict(_parse_resolver(resolver))


def get_urls_as_json(resolver=None):
    resolver = resolver or get_resolver()
    return json.dumps(get_urls_as_dict(resolver))


def _parse_resolver(
    resolver, current_namespace=None, url_prefix=None, include_all=False
):
    allowed_urls = htk_setting('HTK_APPS_JS_URLS_ALLOWED')
    namespace = (
        f"{current_namespace}:{resolver.namespace}"
        if current_namespace
        else resolver.namespace
    )
    include_all = include_all or (namespace in allowed_urls)

    urls = []
    for url_pattern in resolver.url_patterns:
        if isinstance(url_pattern, URLResolver):
            new_url_prefix = _prepare_url_part(url_pattern)
            new_url_prefix = (
                "/" + new_url_prefix
                if url_prefix is None
                else urljoin(url_prefix or "/", new_url_prefix)
            )

            urls += _parse_resolver(
                url_pattern,
                current_namespace=current_namespace,
                url_prefix=new_url_prefix,
                include_all=include_all,
            )
        elif isinstance(url_pattern, URLPattern) and url_pattern.name:
            url_name = (
                f"{namespace}:{url_pattern.name}"
                if namespace
                else url_pattern.name
            )
            if url_name in allowed_urls or include_all:
                full_url = _prepare_url_part(url_pattern)
                urls.append((url_name, urljoin(url_prefix or "/", full_url)))

    return urls


def _prepare_url_part(url_pattern):
    url = ""

    if hasattr(
        url_pattern, "regex"
    ):  # pragma: no cover, NOTE: Django < 2.0 compatibility
        url = url_pattern.regex.pattern
    elif isinstance(url_pattern.pattern, RegexPattern):
        url = url_pattern.pattern._regex
    elif isinstance(url_pattern.pattern, RoutePattern):
        url = url_pattern.pattern._route

    final_url = replace(url, [("^", ""), ("$", "")])

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
        replace(final_url, [(el[0], "{0}") for el in kwarg_matches])
        if kwarg_matches
        else final_url
    )

    # Identifies unnamed URL arguments inside the URL pattern.
    args_matches = URL_ARG_RE.findall(final_url)
    final_url = (
        replace(final_url, [(el, "{0}") for el in args_matches])
        if args_matches
        else final_url
    )

    # Identifies path expression and associated converters inside the URL pattern.
    path_matches = URL_PATH_RE.findall(final_url)
    final_url = (
        replace(final_url, [(el, "{0}") for el in path_matches])
        if (path_matches and not (kwarg_matches or args_matches))
        else final_url
    )

    return final_url
