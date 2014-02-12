from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

import htk.apps.accounts.views as views

urlpatterns = patterns(
    '',
    # account registration and activation
    #url(r'^confirm_email/([a-z0-9]+)$', views.confirm_email, name='account_confirm_email'),
    # password reset
    #url(r'^reset_password$', views.reset_password, name='account_reset_password'),
)
