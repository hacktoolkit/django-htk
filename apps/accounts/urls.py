from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

import htk.apps.accounts.views as views

urlpatterns = patterns(
    '',
    # account registration and activation
    # url(r'^register_social_email$', views.register_social_email, name='account_register_social_email'),
    # url(r'^register_social_login$', views.register_social_login, name='account_register_social_login'),
    # url(r'^register_social_already_linked$', views.register_social_already_linked, name='account_register_social_already_linked'),
    # url(r'^register$', views.register, name='account_register'),
    # url(r'^register_done$', views.register_done, name='account_register_done'),
    # url(r'^resend_confirmation$', views.resend_confirmation, name='account_resend_confirmation'),
    # url(r'^confirm_email/([a-z0-9]+)$', views.confirm_email, name='account_confirm_email'),
    # password reset
    # url(r'^forgot_password$', views.forgot_password, name='account_forgot_password'),
    # url(r'^password_reset_done', views.password_reset_done, name='account_password_reset_done'),
    # url(r'^reset_password$', views.reset_password, name='account_reset_password'),
    # url(r'^password_reset_success', views.password_reset_success, name='account_password_reset_success'),
)
