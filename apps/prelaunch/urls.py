from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

from htk.apps.prelaunch.constants import *
import htk.apps.prelaunch.views as views

urlpatterns = patterns(
    '',
    url(r'^$', views.prelaunch, name=HTK_PRELAUNCH_URL_NAME),
)
