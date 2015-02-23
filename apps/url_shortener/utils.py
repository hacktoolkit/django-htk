from django.db.models import Q

from htk.apps.url_shortener.constants import *
from htk.apps.url_shortener.models import HTKShortUrl
from htk.utils.base_converters import base62_encode
from htk.utils.base_converters import base62_decode

def pre_encode(raw_id):
    """Compute the pre-encoded value

    offset = base^(min_chars - 1)
    n = raw_id
    Prepared value = n^2 - 2n + 1 + offset
    """
    n = raw_id
    offset = HTK_URL_SHORTENER_ENCODER_BASE ** (HTK_URL_SHORTENER_MIN_CHARS - 1)
    prepared = (n * n - 2 * n + 1) + offset
    return prepared

def resolve_raw_id(prepared_id):
    """Resolve `prepared_id` into `raw_id`

    Assume `prepared_id` calculated using pre_encode
    """
    from htk.utils.maths import quadratic
    offset = HTK_URL_SHORTENER_ENCODER_BASE ** (HTK_URL_SHORTENER_MIN_CHARS - 1)
    root = quadratic(1, -2, 1 - (prepared_id - offset))
    if int(root) == root:
        raw_id = root
    else:
        # not a perfect square
        raw_id = None
    return raw_id

def generate_short_url_code(raw_id):
    """Generate the short url code for a `raw_id`
    """
    prepared = pre_encode(raw_id)
    code = base62_encode(prepared)
    return code

def resolve_short_url_code(host, code):
    try:
        prepared_id = base62_decode(code)
        raw_id = resolve_raw_id(prepared_id)
        short_url = HTKShortUrl.objects.get(id=raw_id)
    except HTKShortUrl.DoesNotExist:
        short_url = None
    return short_url

def get_recently_shortened(user=None):
    """Get recently shortened URLs
    """
    short_urls = HTKShortUrl.objects.all()
    return short_urls
