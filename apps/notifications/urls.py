# Django Imports
from django.urls import include
from django.urls import re_path

# HTK Imports
import htk.apps.notifications.views as views


urlpatterns = (
    # re_path(r'^dismiss_alert$', views.dismiss_alert, name='api_dismiss_alert'),
)
