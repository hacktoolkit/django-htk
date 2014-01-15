from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

import htk.views as views

urlpatterns = patterns(
    '',
    # google site verification
    url(r'^google(?P<code>[a-z0-9]+)\.html$', views.google_site_verification, name='google_site_verification'),
    url(r'^BingSiteAuth\.xml$', views.bing_site_auth, name='bing_site_auth'),
    url(r'^(?P<code>.+)--\.html$', views.html_site_verification, name='html_site_verification'),
    url(r'^robots\.txt$', views.robots, name='robots'),
)
