from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.views.decorators.cache import cache_page

import htk.apps.cpq.views as views

urlpatterns = patterns(
    '',
    # public views
    url(r'^invoices/$', views.index, name='cpq_invoices_index'),
    url(r'^invoices/(?P<invoice_code>[a-z0-9]+)$', views.invoice, name='cpq_invoices_invoice'),
    url(r'^groupquotes/$', views.index, name='cpq_groupquotes_index'),
    url(r'^groupquotes/(?P<quote_code>[a-z0-9]+)$', views.groupquote, name='cpq_groupquotes_quote'),
    url(r'^quotes/$', views.index, name='cpq_quotes_index'),
    url(r'^quotes/(?P<quote_code>[a-z0-9]+)$', views.quote, name='cpq_quotes_quote'),
    url(r'^quotes/(?P<quote_code>[a-z0-9]+)/pay$', views.quote_pay, name='cpq_quotes_quote_pay'),
    # admin views
    url(r'^cpq/$', views.index, name='cpq_index'),
    url(r'^cpq/dashboard$', views.dashboard, name='cpq_dashboard'),
    url(r'^cpq/receivables$', views.receivables, name='cpq_receivables'),
    url(r'^cpq/receivables/(?P<year>[0-9]{4})$', views.receivables, name='cpq_receivables_by_year'),
    url(r'^cpq/import_customers$', views.import_customers, name='cpq_import_customers'),
)
