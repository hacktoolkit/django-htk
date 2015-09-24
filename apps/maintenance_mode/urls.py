from django.conf.urls import patterns
from django.conf.urls import url

import htk.apps.maintenance_mode.views as views

urlpatterns = patterns(
    '',
    url(r'^maintenance$', views.maintenance_mode, name='maintenance_mode'),
)
