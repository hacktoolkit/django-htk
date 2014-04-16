import urllib

from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.base import Library
from django.utils.html import escape

from htk.lib.gravatar.utils import get_gravatar_hash

GRAVATAR_URL_PREFIX = getattr(settings, 'GRAVATAR_URL_PREFIX', 'http://www.gravatar.com/')
GRAVATAR_DEFAULT_IMAGE = getattr(settings, 'GRAVATAR_DEFAULT_IMAGE', '')

register = Library()

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
def gravatar_for_email(email, size=80):
    """
    https://en.gravatar.com/site/implement/images/
    """
    url = '%savatar/%s?' % (
        GRAVATAR_URL_PREFIX,
        get_gravatar_hash(email),
    )
    url += urllib.urlencode(
        {
            's': str(size),
            #'default': GRAVATAR_DEFAULT_IMAGE,
        }
    )
    url = escape(url)
    return url

@register.simple_tag
def gravatar_for_user(user, size=80):
    user = get_user(user)
    url = gravatar_for_email(user.email, size=size)
    return url

@register.simple_tag
def gravatar_img_for_email(email, size=80):
    url = gravatar_for_email(email, size)
    img = '<img src="%s" height="%s" width="%s" />' % (
        escape(url),
        size,
        size,
    )
    return img

@register.simple_tag
def gravatar_img_for_user(user, size=80):
    user = get_user(user)
    url = gravatar_for_user(user, size=size)
    img = '<img src="%s" alt="Gravatar for %s" height="%s" width="%s" />' % (
        escape(url),
        user.username,
        size,
        size,
    )
    return img

@register.simple_tag
def gravatar(user, size=80):
    # backward compatibility
    img = gravatar_img_for_user(user, size=size)
    return img
