from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from itertools import chain

from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically

Product = resolve_model_dynamically(htk_setting('HTK_STORE_PRODUCT_MODEL'))
ProductCollection = resolve_model_dynamically(htk_setting('HTK_STORE_PRODUCT_COLLECTION_MODEL'))

class HtkStoreSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        static_view_names = [
            'store',
            'store_collections',
            'store_products',
        ]
        products = Product.objects.all()
        product_collections = ProductCollection.objects.all()
        _items = list(chain(
            static_view_names,
            products,
            product_collections
        ))
        return _items

    def location(self, obj):
        if type(obj) == str:
            path = reverse(obj)
        else:
            path = obj.get_absolute_url()
        return path
