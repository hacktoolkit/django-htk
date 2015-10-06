from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.views.decorators.cache import cache_page

import htk.apps.cpq.views as views

urlpatterns = patterns(
    '',
    url(r'^invoices/$', views.index, name='invoices_index'),
    url(r'^invoices/(?P<invoice_code>[a-z0-9]+)$', views.invoice, name='invoices_invoice'),
    url(r'^quotes/$', views.index, name='quotes_index'),
    url(r'^quotes/(?P<quote_code>[a-z0-9]+)$', views.quote, name='quotes_quote'),
)
