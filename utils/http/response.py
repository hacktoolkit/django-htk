# Django Imports
from django.http import HttpResponse


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
    """
    Set cache headers on a Django HttpResponse.

    Args:
        response (HttpResponse): The response object to modify.
        etag (str, optional): Value for the ETag header.
        expires (int, optional): Seconds until expiration (default 24 hours).
        immutable (bool, optional): Whether to add 'immutable' to Cache-Control.
        vary (str, optional): Value for the Vary header.
        cache_control (str, optional): Override Cache-Control header entirely.
    """
    if cache_control is None:
        cache_control = f"public, max-age={expires}"
        if immutable:
            cache_control += ", immutable"
    response['Cache-Control'] = cache_control
    if vary:
        response['Vary'] = vary
    if etag:
        response['ETag'] = etag
    # Expires header (RFC 7234)
    # Python Standard Library Imports
    from datetime import (
        datetime,
        timedelta,
    )

    expires_date = datetime.utcnow() + timedelta(seconds=expires)
    response['Expires'] = expires_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
    return response


def set_cors_headers_for_image(response):
    """
    Set CORS headers on a Django HttpResponse for image responses.
    """
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
    response['Access-Control-Allow-Headers'] = (
        'Accept, Accept-Language, Content-Language, Content-Type'
    )
    response['Access-Control-Max-Age'] = '86400'  # 24 hours
    return response
