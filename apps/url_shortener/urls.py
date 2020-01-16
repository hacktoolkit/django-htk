# Django Imports
from django.conf.urls import include
from django.conf.urls import url

# HTK Imports
import htk.apps.url_shortener.views as views
from htk.apps.url_shortener.constants import *
from htk.utils import htk_setting


URL_SHORTENER_PREFIX = htk_setting('HTK_URL_SHORTENER_PREFIX', '')

urlpatterns = (
    url(r'^%s(?P<code>[A-Za-z0-9]{%d,%d})$' % (
        URL_SHORTENER_PREFIX,
        HTK_URL_SHORTENER_MIN_CHARS,
        HTK_URL_SHORTENER_MAX_CHARS,
    ), views.short_url, name='shorturl'),
)
