from django.conf import settings
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

import htk.views as views

urlpatterns = patterns(
    '',
    url(r'^robots\.txt$', views.robots, name='robots'),
    url(r'^google(?P<code>[a-z0-9]+)\.html$', views.google_site_verification, name='google_site_verification'),
    url(r'^(?P<code>.+)--\.html$', views.html_site_verification, name='html_site_verification'),
    url(r'^BingSiteAuth\.xml$', views.bing_site_auth, name='bing_site_auth'),
    url(r'^redir$', views.redir, name='redir'),
)

if settings.TEST or settings.ENV_DEV:
    urlpatterns += patterns(
        '',
        url(r'^403$', views.error_view, name='error_403'),
        url(r'^404$', views.error_view, name='error_404'),
        url(r'^500$', views.error_view, name='error_500'),
    )
