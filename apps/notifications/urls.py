from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

import htk.apps.notifications.views as views

urlpatterns = patterns(
    '',
    # url(r'^dismiss_alert$', views.dismiss_alert, name='api_dismiss_alert'),
)
