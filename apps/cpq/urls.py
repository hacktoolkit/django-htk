# Django Imports
from django.urls import include
from django.urls import re_path
from django.views.decorators.cache import cache_page

# HTK Imports
import htk.apps.cpq.views as views


urlpatterns = (
    # public views
    re_path(r'^invoices/$', views.index, name='cpq_invoices_index'),
    re_path(r'^invoices/(?P<invoice_code>[a-z0-9]+)$', views.invoice, name='cpq_invoices_invoice'),
    re_path(r'^groupquotes/$', views.index, name='cpq_groupquotes_index'),
    re_path(r'^groupquotes/(?P<quote_code>[a-z0-9]+)$', views.groupquote, name='cpq_groupquotes_quote'),
    re_path(r'^groupquotes/(?P<quote_code>[a-z0-9]+)/all$', views.groupquote_all, name='cpq_groupquotes_quote_all'),
    re_path(r'^quotes/$', views.index, name='cpq_quotes_index'),
    re_path(r'^quotes/(?P<quote_code>[a-z0-9]+)$', views.quote, name='cpq_quotes_quote'),
    re_path(r'^quotes/(?P<quote_code>[a-z0-9]+)/pay$', views.quote_pay, name='cpq_quotes_quote_pay'),
    # admin views
    re_path(r'^cpq/$', views.index, name='cpq_index'),
    re_path(r'^cpq/dashboard$', views.dashboard, name='cpq_dashboard'),
    re_path(r'^cpq/receivables$', views.receivables, name='cpq_receivables'),
    re_path(r'^cpq/receivables/(?P<year>[0-9]{4})$', views.receivables, name='cpq_receivables_by_year'),
    re_path(r'^cpq/import_customers$', views.import_customers, name='cpq_import_customers'),
)
