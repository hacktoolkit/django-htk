import urllib

from django import template
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.html import escape
from django.utils.safestring import mark_safe

from htk.lib.gravatar.utils import get_gravatar_hash

# http://en.gravatar.com/site/implement/images/
GRAVATAR_URL_PROTOCOL = 'https://' if settings.SECURE_SSL_HOST or settings.SECURE_SSL_REDIRECT else 'http://'
GRAVATAR_URL_PREFIX = getattr(settings, 'GRAVATAR_URL_PREFIX', '%s%s' % (GRAVATAR_URL_PROTOCOL, '//www.gravatar.com',))
GRAVATAR_DEFAULT_IMAGE = getattr(settings, 'GRAVATAR_DEFAULT_IMAGE', 'mm')
GRAVATAR_DEFAULT_SIZE = 80

register = template.Library()


def get_user(user):
    UserModel = get_user_model()
    if not isinstance(user, UserModel):
        try:
            user = UserModel.objects.get(username=user)
        except UserModel.DoesNotExist:
            # TODO: make better? smarter? strong? maybe give it wheaties?
            raise Exception, 'Bad user for gravatar.'
    return user

@register.simple_tag
def gravatar_for_email(email, size=GRAVATAR_DEFAULT_SIZE):
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

@register.simple_tag
def gravatar_for_user(user, size=GRAVATAR_DEFAULT_SIZE):
    user = get_user(user)
    url = gravatar_for_email(user.profile.confirmed_email or user.email, size=size)
    return url

@register.simple_tag
def gravatar_img_for_email(email, size=GRAVATAR_DEFAULT_SIZE):
    url = gravatar_for_email(email, size)
    img = '<img src="%s" height="%s" width="%s" />' % (
        escape(url),
        size,
        size,
    )
    return img

@register.simple_tag
def gravatar_img_for_user(user, size=GRAVATAR_DEFAULT_SIZE):
    user = get_user(user)
    url = gravatar_for_user(user, size=size)
    img = '<img src="%s" alt="Gravatar for %s" height="%s" width="%s" />' % (
        escape(url),
        user.profile.get_display_name(),
        size,
        size,
    )
    img = mark_safe(img)
    return img

@register.simple_tag
def gravatar(user, size=GRAVATAR_DEFAULT_SIZE):
    # backward compatibility
    img = gravatar_img_for_user(user, size=size)
    return img
