from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.views.decorators.cache import cache_page

import htk.apps.invoices.views as views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='invoices_index'),
    url(r'^(?P<invoice_code>[a-z0-9]+)$', views.invoice, name='invoices_invoice'),
)
