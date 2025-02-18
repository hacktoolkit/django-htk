# Python Standard Library Imports
import re
import typing as T

# Django Imports
from django.http import HttpRequest

# HTK Imports
from htk.utils import htk_setting
from htk.utils.constants import *
from htk.utils.general import strtobool_safe


# isort: off


def get_current_request():
    from htk.middleware.classes import GlobalRequestMiddleware

    request = GlobalRequestMiddleware.get_current_request()
    return request


def is_ajax_request(request):
    # content_type = request.META.get('CONTENT_TYPE') or request.content_type
    requested_with = request.META.get('HTTP_X_REQUESTED_WITH')
    accepts_json = hasattr(request, 'accepts') and request.accepts(
        'application/json'
    )
    accept_mimetypes = request.META.get('HTTP_ACCEPT').split(',')

    is_ajax = (
        requested_with == 'XMLHttpRequest'
        or accepts_json
        or 'application/json' in accept_mimetypes
    )

    return is_ajax


def extract_request_ip(request):
    # copied from django_ratchet.middleware.py
    # some common things passed by load balancers... will need more of these.
    forwarded_for = request.environ.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        forwarded_ips = forwarded_for.split(',')
        # take the last one in the list
        return forwarded_for.split(',')[-1].strip()
    real_ip = request.environ.get('HTTP_X_REAL_IP')
    if real_ip:
        return real_ip
    return request.environ['REMOTE_ADDR']


def extract_request_param(request, param, as_type=str, allow_none=True):
    """Extracts a URL parameter from the request (i.e. request.GET.get)

    - Performs basic input validation and allows typed retrieval via `as_type`
    - Can designate whether `None` is allowed via `allow_none`
    """
    default_value_map = {
        str: '',
        bool: False,
        int: 0,
        float: 0,
    }
    default_value = None if allow_none else default_value_map.get(as_type, '')

    raw_value = request.GET.get(param, default_value)

    if as_type == str:
        value = raw_value
    elif as_type == bool:
        value = (
            None
            if (raw_value is None and allow_none)
            else strtobool_safe(raw_value)
        )
    elif as_type == int:
        m = (
            re.match(r'^(?:\+|\-)?(?P<value>\d+)\.?$', raw_value)
            if raw_value
            else None
        )
        value = int(m.group('value')) if m else default_value
    elif as_type == float:
        m = (
            re.match(r'^(?:\+|\-)?(?P<value>\d*\.?\d*)$', raw_value)
            if raw_value
            else None
        )
        value = float(m.group('value')) if m else default_value
    else:
        value = raw_value

    return value


def get_full_url_name(resolver_match):
    """Returns the full URL name for a resolver match

    This method is needed because Django's `resolver_match.url_name`
    does not include namespaces automatically.
    """
    namespaces = ":".join(resolver_match.namespaces)
    full_url_name = (
        f"{namespaces}:{resolver_match.url_name}"
        if namespaces
        else resolver_match.url_name
    )
    return full_url_name


def get_request_metadata(request):
    path = request.path
    url_name = request.resolver_match.url_name
    full_url_name = get_full_url_name(request.resolver_match)
    host = request.get_host()
    is_secure = request.is_secure()
    protocol = 'http' + ('s' if is_secure else '')
    base_uri = '%s://%s' % (
        protocol,
        host,
    )
    full_uri = '%s%s' % (
        base_uri,
        path,
    )

    request_metadata = {
        'request': request,
        'is_secure': is_secure,
        'host': host,
        'path': path,
        'url_name': url_name,
        'full_url_name': full_url_name,
        'protocol': protocol,
        'base_uri': base_uri,
        'full_uri': full_uri,
    }
    return request_metadata


def get_custom_http_headers(request):
    custom_http_headers = []
    for header_name in request.META.keys():
        if (
            re.match(r'^HTTP', header_name)
            and header_name not in REQUEST_HTTP_HEADERS_STANDARD
        ):
            custom_http_headers.append(header_name)
    return custom_http_headers


def build_dict_from_request(request):
    """Build a dictionary from `request` that can be serialized to JSON"""
    user = request.user if request.user.is_authenticated else None
    obj = {
        'request': {
            'GET': request.GET,
            'POST': request.POST,
        },
        'referrer': request.META.get('HTTP_REFERER', ''),
        'user': user,
        'user_id': user.id if user else '',
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        'user_ip': extract_request_ip(request),
    }
    return obj


def is_domain_meta_view(request):
    """Determines whether the request is for a domain meta view

    E.g. Google Site verification, robots.txt, sitemap.xml, etc.
    """
    url_name = request.resolver_match.url_name
    domain_meta_url_names = htk_setting('HTK_DOMAIN_META_URL_NAMES')
    if url_name in domain_meta_url_names:
        return True
    else:
        pass
    return False


def is_allowed_host(host):
    """Determines whether this `host` is explicitly allowed"""
    from django.conf import settings

    allowed = False
    if settings.TEST:
        allowed = True
    else:
        allowed_host_regexps = htk_setting('HTK_ALLOWED_HOST_REGEXPS')
        for host_re in allowed_host_regexps:
            allowed = bool(re.match(host_re, host))
            if allowed:
                break
    return allowed


def parse_authorization_header(
    request: HttpRequest,
) -> tuple[T.Optional[str], T.Optional[str]]:
    """Parse the authorization header from the request

    Expected format: `<token_type> <token>`

    Examples:
    - `Authorization: Bearer <token>`
    - `Authorization: Basic <credentials>`

    Returns:
    - `token_type`: The type of token, e.g. `Bearer` or `Basic`
    - `token`: The token
    """
    token = None
    token_type = None

    if 'HTTP_AUTHORIZATION' in request.META:
        auth_header = request.META['HTTP_AUTHORIZATION']
        parts = auth_header.split()
        if len(parts) == 2:
            token_type, token = parts
        else:
            pass
    else:
        pass

    return token_type, token
