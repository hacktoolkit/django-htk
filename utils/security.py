from django.conf import settings


def should_use_https():
    """Determines whether the current context should use HTTPS
    """
    use_https = settings.SECURE_SSL_HOST or settings.SECURE_SSL_REDIRECT or False

    if not use_https:
        # try to get from request
        from htk.utils.request import get_current_request
        request = get_current_request()

        use_https = request and request.is_secure()

    return use_https
