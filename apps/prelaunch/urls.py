# Django Imports
from django.conf.urls import include
from django.conf.urls import url

# HTK Imports
import htk.apps.prelaunch.views as views
from htk.apps.prelaunch.constants import *
from htk.apps.prelaunch.utils import get_prelaunch_url_name


urlpatterns = (
    url(r'^$', views.prelaunch, name=get_prelaunch_url_name()),
)
