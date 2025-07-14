# Python Standard Library Imports
import datetime

# Django Imports
from django.http import HttpResponse

# HTK Imports
from htk.utils import utcnow


class HttpResponseAccepted(HttpResponse):
    status_code = 202


def set_cache_headers(
    response: HttpResponse,
    *,
    etag: str = None,
    expires: int = 86400,  # seconds
    immutable: bool = True,
    vary: str = 'Accept-Encoding',
    cache_control: str = None,
):
    """Set cache headers on a Django HttpResponse."""
    if cache_control is None:
        cache_control = f"public, max-age={expires}"
        if immutable:
            cache_control += ", immutable"
    response['Cache-Control'] = cache_control
    if vary:
        response['Vary'] = vary
    if etag:
        response['ETag'] = etag

    expires_date = utcnow() + datetime.timedelta(seconds=expires)
    response['Expires'] = expires_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
    return response


def set_cors_headers_for_image(response):
    """Set CORS headers on a Django HttpResponse."""
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
    response['Access-Control-Allow-Headers'] = (
        'Accept, Accept-Language, Content-Language, Content-Type'
    )
    response['Access-Control-Max-Age'] = '86400'  # 24 hours
    return response
