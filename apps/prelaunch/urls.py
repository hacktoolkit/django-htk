from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

from htk.apps.prelaunch.constants import *
from htk.apps.prelaunch.utils import get_prelaunch_url_name

import htk.apps.prelaunch.views as views

urlpatterns = patterns(
    '',
    url(r'^$', views.prelaunch, name=get_prelaunch_url_name()),
)
