# Django Imports
from django.urls import include
from django.urls import re_path

# HTK Imports
import htk.apps.accounts.views as views


urlpatterns = (
    # account registration and activation
    # re_path(r'^register_social_email$', views.register_social_email, name='account_register_social_email'),
    # re_path(r'^register_social_login$', views.register_social_login, name='account_register_social_login'),
    # re_path(r'^register_social_already_linked$', views.register_social_already_linked, name='account_register_social_already_linked'),
    # re_path(r'^register$', views.register, name='account_register'),
    # re_path(r'^register_done$', views.register_done, name='account_register_done'),
    # re_path(r'^resend_confirmation$', views.resend_confirmation, name='account_resend_confirmation'),
    # re_path(r'^confirm_email/([a-z0-9]+)$', views.confirm_email, name='account_confirm_email'),
    # password reset
    # re_path(r'^forgot_password$', views.forgot_password, name='account_forgot_password'),
    # re_path(r'^password_reset_done', views.password_reset_done, name='account_password_reset_done'),
    # re_path(r'^reset_password$', views.reset_password, name='account_reset_password'),
    # re_path(r'^password_reset_success', views.password_reset_success, name='account_password_reset_success'),
)
