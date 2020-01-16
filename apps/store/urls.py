# Django Imports
from django.conf.urls import include
from django.conf.urls import url
from django.views.decorators.cache import cache_page

# HTK Imports
import htk.apps.store.views as views


urlpatterns = (
    url(r'^$', views.index, name='store'),
    url(r'^collections/$', views.product_collections, name='store_collections'),
    url(r'^collections/(?P<collection_id>[0-9]+)/(?P<seo_title>.*)$', views.product_collection_view, name='store_collection'),
    url(r'^products/$', views.products, name='store_products'),
    url(r'^products/(?P<product_id>[0-9]+)/(?P<seo_title>.*)$', views.product, name='store_product'),
)
