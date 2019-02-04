# Python Standard Library Imports
import hashlib
import urllib

# Third Party / PIP Imports

# Django Imports
from django.conf import settings

# HTK Imports


# http://en.gravatar.com/site/implement/images/
GRAVATAR_URL_PROTOCOL = 'https' if settings.SECURE_SSL_HOST or settings.SECURE_SSL_REDIRECT else 'http'
GRAVATAR_URL_PREFIX = getattr(settings, 'GRAVATAR_URL_PREFIX', '%s://%s' % (GRAVATAR_URL_PROTOCOL, 'www.gravatar.com',))
GRAVATAR_DEFAULT_IMAGE = getattr(settings, 'GRAVATAR_DEFAULT_IMAGE', 'mm')
GRAVATAR_DEFAULT_SIZE = 80


def get_gravatar_hash(email):
    """Creates a Gravatar hash

    http://en.gravatar.com/site/implement/hash/
    """
    gravatar_hash = hashlib.md5(email.strip().lower()).hexdigest()
    return gravatar_hash


def get_gravatar_for_email(email, size=GRAVATAR_DEFAULT_SIZE):
    """
    https://en.gravatar.com/site/implement/images/
    """
    try:
        size = int(size)
    except ValueError:
        size = GRAVATAR_DEFAULT_SIZE

    url = '%s/avatar/%s?' % (
        GRAVATAR_URL_PREFIX,
        get_gravatar_hash(email),
    )
    url += urllib.urlencode(
        {
            's': str(size),
            'default': GRAVATAR_DEFAULT_IMAGE,
        }
    )
    return url
