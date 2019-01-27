from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url

import htk.views as views

urlpatterns = (
    url(r'^health_check$', views.health_check, name='health_check'),
    url(r'^robots\.txt$', views.robots, name='robots'),
    url(r'^google(?P<code>[a-z0-9]+)\.html$', views.google_site_verification, name='google_site_verification'),
    url(r'^(?P<code>.+)--\.html$', views.html_site_verification, name='html_site_verification'),
    url(r'^BingSiteAuth\.xml$', views.bing_site_auth, name='bing_site_auth'),
    url(r'^redir$', views.redir, name='redir'),
)

if 'htk.apps.maintenance_mode' in settings.INSTALLED_APPS:
    urlpatterns += (
        url(r'', include('htk.apps.maintenance_mode.urls')),
    )

if settings.TEST or settings.ENV_DEV:
    urlpatterns += (
        url(r'^400$', views.error_view, name='error_400'),
        url(r'^403$', views.error_view, name='error_403'),
        url(r'^404$', views.error_view, name='error_404'),
        url(r'^500$', views.error_view, name='error_500'),
        url(r'^browser_info$', views.browser_info, name='tools_browser_info'),
        url(r'^debugger$', views.debugger, name='tools_debugger'),
    )
