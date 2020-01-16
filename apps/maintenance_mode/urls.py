# Django Imports
from django.conf.urls import url

# HTK Imports
import htk.apps.maintenance_mode.views as views


urlpatterns = (
    url(r'^maintenance$', views.maintenance_mode, name='maintenance_mode'),
)
