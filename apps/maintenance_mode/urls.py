from django.conf.urls import url

import htk.apps.maintenance_mode.views as views

urlpatterns = (
    url(r'^maintenance$', views.maintenance_mode, name='maintenance_mode'),
)
