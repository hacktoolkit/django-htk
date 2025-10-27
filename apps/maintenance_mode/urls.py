# Django Imports
from django.urls import re_path

# HTK Imports
import htk.apps.maintenance_mode.views as views


urlpatterns = (
    re_path(r'^maintenance$', views.maintenance_mode, name='maintenance_mode'),
)
