# Django Imports
from django.urls import include
from django.urls import re_path
from django.views.decorators.cache import cache_page

# HTK Imports
import htk.apps.store.views as views


urlpatterns = (
    re_path(r'^$', views.index, name='store'),
    re_path(r'^collections/$', views.product_collections, name='store_collections'),
    re_path(r'^collections/(?P<collection_id>[0-9]+)/(?P<seo_title>.*)$', views.product_collection_view, name='store_collection'),
    re_path(r'^products/$', views.products, name='store_products'),
    re_path(r'^products/(?P<product_id>[0-9]+)/(?P<seo_title>.*)$', views.product, name='store_product'),
)
