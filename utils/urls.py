# Third Party (PyPI) Imports
import requests

# Django Imports
from django.urls import reverse


def reverse_with_query_params(viewname, query_params, urlconf=None, args=None, kwargs=None, current_app=None):
    """Wrapper for `reverse()` that appends GET query parameters `query_params`
    """
    base_url = reverse(viewname, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    url = build_url_with_query_params(base_url, query_params)
    return url

def build_url_with_query_params(base_url, query_params):
    """Builds a URL with GET query parameters `query_params`
    """
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
        url = '%s?%s' % (base_url, query,)

    return url
