# Django Imports
from django.urls import include
from django.urls import re_path

# HTK Imports
import htk.apps.prelaunch.views as views
from htk.apps.prelaunch.constants import *
from htk.apps.prelaunch.utils import get_prelaunch_url_name


urlpatterns = (
    re_path(r'^$', views.prelaunch, name=get_prelaunch_url_name()),
)
