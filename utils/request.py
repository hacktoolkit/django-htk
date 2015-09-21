import re

from htk.utils import htk_setting
from htk.utils.constants import *

def get_current_request():
    from htk.middleware.classes import GlobalRequestMiddleware
    request = GlobalRequestMiddleware.get_current_request()
    return request

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

def get_custom_http_headers(request):
    custom_http_headers = []
    for header_name in request.META.keys():
        if re.match(r'^HTTP', header_name) and header_name not in REQUEST_HTTP_HEADERS_STANDARD:
            custom_http_headers.append(header_name)
    return custom_http_headers

def build_dict_from_request(request):
    """Build a dictionary from `request` that can be serialized to JSON
    """
    user = request.user if request.user.is_authenticated() else None
    obj = {
        'request' : {
            'GET' : request.GET,
            'POST' : request.POST,
        },
        'referrer' : request.META.get('HTTP_REFERER', ''),
        'user' : user,
        'user_id' : user.id if user else '',
        'user_agent' : request.META.get('HTTP_USER_AGENT', ''),
        'user_ip' : extract_request_ip(request),
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
