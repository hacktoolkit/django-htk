# Python Standard Library Imports
import hashlib

# Third Party (PyPI) Imports
import requests
import six.moves.urllib as urllib

# Django Imports
from django.conf import settings


# http://en.gravatar.com/site/implement/images/
GRAVATAR_URL_PROTOCOL = 'https' if settings.SECURE_SSL_HOST or settings.SECURE_SSL_REDIRECT else 'http'
GRAVATAR_URL_PREFIX = getattr(settings, 'GRAVATAR_URL_PREFIX', '%s://%s' % (GRAVATAR_URL_PROTOCOL, 'www.gravatar.com',))
GRAVATAR_DEFAULT_IMAGE = getattr(settings, 'GRAVATAR_DEFAULT_IMAGE', 'mp')
GRAVATAR_DEFAULT_SIZE = 80


def get_gravatar_hash(email):
    """Creates a Gravatar hash

    http://en.gravatar.com/site/implement/hash/
    """
    gravatar_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
    return gravatar_hash


def get_gravatar_for_email(email, size=GRAVATAR_DEFAULT_SIZE, default=GRAVATAR_DEFAULT_IMAGE):
    return build_gravatar_url_for_email(email, size=GRAVATAR_DEFAULT_SIZE, default=GRAVATAR_DEFAULT_IMAGE)


def build_gravatar_url_for_email(email, size=GRAVATAR_DEFAULT_SIZE, default=GRAVATAR_DEFAULT_IMAGE):
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
    url += urllib.parse.urlencode(
        {
            's': str(size),
            'default': default,
        }
    )
    return url


def has_gravatar(email):
    url = get_gravatar_for_email(email, default='404')
    response = requests.get(url)
    has_gravatar = response.status_code == 200
    return has_gravatar
