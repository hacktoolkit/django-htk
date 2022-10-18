# Third Party (PyPI) Imports
import requests

# Django Imports
from django.urls import reverse

# HTK Imports
from htk.utils import htk_setting


def reverse_with_query_params(
    viewname,
    query_params,
    urlconf=None,
    args=None,
    kwargs=None,
    current_app=None,
):
    """Wrapper for `reverse()` that appends GET query parameters `query_params`"""
    base_url = reverse(
        viewname,
        urlconf=urlconf,
        args=args,
        kwargs=kwargs,
        current_app=current_app,
    )
    url = build_url_with_query_params(base_url, query_params)
    return url


def build_url_with_query_params(base_url, query_params):
    """Builds a URL with GET query parameters `query_params`"""
    try:
        r = requests.PreparedRequest()
        r.prepare_url(base_url, query_params)
        url = r.url
    except requests.exceptions.MissingSchema:
        # `base_url` isn't a full URL, use another placeholder just to generate the query portion
        r = requests.PreparedRequest()
        r.prepare_url('http://hacktoolkit.com', query_params)
        temp_url = r.url
        url_parts = temp_url.split('?')
        query = url_parts[1] if len(url_parts) == 2 else None
        url = '%s?%s' % (
            base_url,
            query,
        )

    return url


def build_full_url(partial_url, request=None, use_secure=True):
    protocol = 'https' if use_secure else 'http'
    request_domain = request.get_host() if request else None
    domain = request_domain or htk_setting('HTK_DEFAULT_DOMAIN')

    full_url = '{}://{}{}'.format(protocol, domain, partial_url)
    return full_url
