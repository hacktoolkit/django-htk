from itertools import chain

from htk.sitemaps import HtkBaseSitemap
from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically

Product = resolve_model_dynamically(htk_setting('HTK_STORE_PRODUCT_MODEL'))
ProductCollection = resolve_model_dynamically(htk_setting('HTK_STORE_PRODUCT_COLLECTION_MODEL'))

class HtkStoreSitemap(HtkBaseSitemap):
    priority = 0.5
    changefreq = 'daily'

    def get_static_view_names(self):
        static_view_names = [
            'store',
            'store_collections',
            'store_products',
        ]
        return static_view_names

    def get_model_instances(self):
        products = Product.objects.all()
        product_collections = ProductCollection.objects.all()
        _instances = chain(
            products,
            product_collections,
        )
        return _instances
