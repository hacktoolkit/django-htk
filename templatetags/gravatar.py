import hashlib
import urllib

from django import template
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.html import escape

UserModel = get_user_model()

GRAVATAR_URL_PREFIX = getattr(settings, 'GRAVATAR_URL_PREFIX', 'http://www.gravatar.com/')
GRAVATAR_DEFAULT_IMAGE = getattr(settings, 'GRAVATAR_DEFAULT_IMAGE', '')

register = template.Library()

def get_user(user):
    if not isinstance(user, UserModel):
        try:
            user = UserModel.objects.get(username=user)
        except UserModel.DoesNotExist:
            # TODO: make better? smarter? strong? maybe give it wheaties?
            raise Exception, 'Bad user for gravatar.'
    return user

def gravatar_for_email(email, size=80):
    """
    https://en.gravatar.com/site/implement/images/
    """
    url = '%savatar/%s?' % (
        GRAVATAR_URL_PREFIX,
        hashlib.md5(email).hexdigest(),
    )
    url += urllib.urlencode(
        {
            's': str(size),
            #'default': GRAVATAR_DEFAULT_IMAGE,
        }
    )
    url = escape(url)
    return url

def gravatar_for_user(user, size=80):
    user = get_user(user)
    url = gravatar_for_email(user.email, size)
    return url

def gravatar_img_for_email(email, size=80):
    url = gravatar_for_email(email, size)
    img = '<img src="%s" height="%s" width="%s" />' % (
        escape(url),
        size,
        size,
    )
    return img

def gravatar_img_for_user(user, size=80):
    user = get_user(user)
    url = gravatar_for_user(user)
    img = '<img src="%s" alt="Gravatar for %s" height="%s" width="%s" />' % (
        escape(url),
        user.username,
        size,
        size,
    )
    return img

def gravatar(user, size=80):
    # backward compatibility
    img = gravatar_img_for_user(user, size)
    return img

register.simple_tag(gravatar)
register.simple_tag(gravatar_for_user)
register.simple_tag(gravatar_for_email)
register.simple_tag(gravatar_img_for_user)
register.simple_tag(gravatar_img_for_email)
