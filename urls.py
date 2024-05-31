# Django Imports
from django.conf import settings
from django.urls import (
    include,
    re_path,
)

# HTK Imports
import htk.views as views


urlpatterns = (
    re_path(r'^health_check$', views.health_check, name='health_check'),
    re_path(r'^robots\.txt$', views.robots, name='robots'),
    re_path(
        r'^google(?P<code>[a-z0-9]+)\.html$',
        views.google_site_verification,
        name='google_site_verification',
    ),
    re_path(
        r'^(?P<code>.+)--\.html$',
        views.html_site_verification,
        name='html_site_verification',
    ),
    re_path(
        r'^BingSiteAuth\.xml$', views.bing_site_auth, name='bing_site_auth'
    ),
    re_path(
        r'^.well-known/brave-rewards-verification.txt$',
        views.brave_rewards_verification,
        name='brave_rewards_verification',
    ),
    re_path(r'^redir$', views.redir, name='redir'),
)

if 'htk.apps.maintenance_mode' in settings.INSTALLED_APPS:
    urlpatterns += (re_path(r'', include('htk.apps.maintenance_mode.urls')),)

if settings.TEST or settings.ENV_DEV:
    urlpatterns += (
        re_path(r'^400$', views.error_view, name='error_400'),
        re_path(r'^403$', views.error_view, name='error_403'),
        re_path(r'^404$', views.error_view, name='error_404'),
        re_path(r'^500$', views.error_view, name='error_500'),
        re_path(
            r'^browser_info$', views.browser_info, name='tools_browser_info'
        ),
        re_path(r'^debugger$', views.debugger, name='tools_debugger'),
    )
