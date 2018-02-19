import json

from htk.utils import htk_setting
from htk.utils.cache_descriptors import CachedAttribute

class HtkShopifyArchiver(object):
    def __init__(self, api=None):
        if api is None:
            from htk.lib.shopify_lib.utils import get_shopify_api_cli
            api = get_shopify_api_cli()
        self.api = api

    def _get_iterator_for_item_type(self, item_type):
        iterators = {
            'product' : self.api.iter_products,
            'order' : self.api.iter_orders,
            'customer' : self.api.iter_customers,
        }
        iterator = iterators.get(item_type)
        return iterator

    def _get_archiver_for_item_type(self, item_type):
        archivers = {
            'product' : self.archive_product,
            'order' : self.archive_order,
            'customer' : self.archive_customer,
        }
        archiver = archivers.get(item_type)
        return archiver

    def already_cached(self, item_type, item, key):
        """Check whether an `item` of `item_type` was already cached
        `key` is a function that applies to `item` to get the primary key
        """
        cache = self.items_seen[item_type]
        pk = key(item)
        if pk in cache:
            was_cached = True
        else:
            cache[pk] = True
            was_cached = False
        return was_cached

    def archive_all(self):
        # reset the cache
        self.items_seen = {
            'product' : {},
            'product_tag' : {},
            'product_image' : {},
            'product_variant' : {},
            'order' : {},
            'customer' : {},
            'customer_address' : {},
        }
        self.archive_products()
        self.archive_orders()
        self.archive_customers()

    @CachedAttribute
    def fk_item_types(self):
        item_types = (
            'product_tag',
            'product_image',
            'product_variant',
            'customer_address',
        )
        return item_types

    def archive_item_type(self, item_type):
        """Archives a collection of Shopify.Resource of `item_type` using `iterator`
        """
        print 'Archiving %ss' % item_type
        iterator = self._get_iterator_for_item_type(item_type)
        for item, i, total, page in iterator():
            print '%s of %s %ss'  % (i, total, item_type,)
            self.archive_item(item_type, item)

    def archive_products(self):
        self.archive_item_type('product')

    def archive_orders(self):
        self.archive_item_type('order')

    def archive_customers(self):
        self.archive_item_type('customer')

    def archive_item(self, item_type, item):
        """Archives a single Shopify.Resource `item` into some database using `archiver`
        """
        archiver = self._get_archiver_for_item_type(item_type)
        archiver(item_type, item)

    def archive_product(self, item_type, product):
        raise Exception('HtkShopifyArchiver::archive_product not implemented')

    def archive_customer(self, item_type, customer):
        raise Exception('HtkShopifyArchiver::archive_customer not implemented')

    def archive_order(self, item_type, order):
        raise Exception('HtkShopifyArchiver::archive_order not implemented')

class HtkShopifyMongoDBArchiver(HtkShopifyArchiver):
    def __init__(self, mongodb_connection=None, mongodb_name=None, api=None):
        if mongodb_connection is None:
            mongodb_connection = htk_setting('HTK_MONGODB_CONNECTION')
        if mongodb_name is None:
            mongodb_name = htk_setting('HTK_MONGODB_NAME')

        from pymongo import MongoClient
        self.mongo_client = MongoClient(mongodb_connection)
        self.mongo_db = self.mongo_client[mongodb_name]

        super(HtkShopifyMongoDBArchiver, self).__init__(api=api)

    def get_collection_name(self, item_type):
        collections = htk_setting('HTK_SHOPIFY_MONGODB_COLLECTIONS')
        collection_name = collections[item_type]
        return collection_name

    def _get_document_preparator(self, item_type):
        preparators = {
            'product' : self._prepare_product,
            'product_tag' : self._prepare_product_tag,
            'product_image' : self._prepare_product_image,
            'product_variant' : self._prepare_product_variant,
            'order' : self._prepare_order,
            'customer' : self._prepare_customer,
            'customer_address' : self._prepare_customer_address,
        }
        preparator = preparators.get(item_type)
        return preparator

    def upsert(self, item_type, document):
        collection_name = self.get_collection_name(item_type)
        collection = self.mongo_db[collection_name]

        key = lambda document: document['_id']
        pk = key(document)
        if self.already_cached(item_type, document, key):
            if item_type not in self.fk_item_types:
                print 'Skipping duplicate processed in session %s: %s' % (item_type, pk,)
                print document
        else:
            preparator = self._get_document_preparator(item_type)
            if preparator:
                preparator(document)
            collection.replace_one({ '_id' : pk, }, document, upsert=True)

    def _convert_iso_date_fields(self, document, iso_date_fields):
        """Converts ISO date fields to UNIX timestamp
        """
        from htk.utils.datetime_utils import iso_datetime_to_unix_time
        for field in iso_date_fields:
            value = document.get(field)
            if value is not None:
                field_name = field[:-3] if field.endswith('_at') else field
                key = '%s_%s' % (field_name, 'timestamp',)
                timestamp = iso_datetime_to_unix_time(value)
                document[key] = timestamp

    def archive_product(self, item_type, product):
        document = json.loads(product.to_json())[item_type]
        pk = document['id']
        document['_id'] = pk
        del document['id']

        # lift sku from first variant
        sku = document.get('variants', [{}])[0].get('sku')
        document['sku'] = sku

        # rewrite tags as array
        tags_str = document['tags']
        tags = [tag.strip() for tag in tags_str.split(',')]
        for tag in tags:
            self._archive_product_tag('product_tag', tag)
        document['tags'] = tags

        # rewrite images as foreign key
        product_image = document['image']
        image_id = self._archive_product_image('product_image', product_image)
        document['image_id'] = image_id
        del document['image']
        # images -> image_ids (fk)
        image_ids = [self._archive_product_image('product_image', product_image) for product_image in document.get('images', [])]
        document['image_ids'] = image_ids
        del document['images']

        # rewrite variants as foreign key
        variant_ids = [self._archive_product_variant('product_variant', product_variant) for product_variant in document.get('variants', [])]
        document['variant_ids'] = variant_ids
        del document['variants']
        variant_id = variant_ids[0] if len(variant_ids) else None
        document['variant_id'] = variant_id

        self.upsert(item_type, document)
        return pk

    def _archive_product_tag(self, item_type, tag):
        document = {
            '_id' : tag,
        }

        self.upsert(item_type, document)
        return tag

    def _archive_product_image(self, item_type, document):
        pk = document['id']
        document['_id'] = pk
        del document['id']

        self.upsert(item_type, document)
        return pk

    def _archive_product_variant(self, item_type, document):
        pk = document['id']
        document['_id'] = pk
        del document['id']

        self.upsert(item_type, document)
        return pk

    def archive_customer(self, item_type, customer):
        document = json.loads(customer.to_json())[item_type]
        pk = document['id']
        document['_id'] = pk
        del document['id']

        # rewrite addresses as foreign key
        default_address = document.pop('default_address', None)
        default_address_id = self._archive_customer_address('customer_address', default_address) if default_address else None
        document['default_address_id'] = default_address_id
        # addresses -> address_ids (fk)
        address_ids = [self._archive_customer_address('customer_address', customer_address) for customer_address in document.get('addresses', [])]
        document['address_ids'] = address_ids
        del document['addresses']

        self.upsert(item_type, document)
        return pk

    def _archive_customer_address(self, item_type, document):
        pk = document['id']
        document['_id'] = pk
        del document['id']

        self.upsert(item_type, document)
        return pk

    def archive_order(self, item_type, order):
        document = json.loads(order.to_json())[item_type]
        pk = document['id']
        document['_id'] = pk
        del document['id']

        # rewrite customer as foreign key
        customer_id = document['customer']['id']
        document['customer_id'] = customer_id
        del document['customer']

        self.upsert(item_type, document)
        return pk

    ##
    # Preparation methods

    def _prepare_product(self, document):
        self._convert_iso_date_fields(document, ['updated_at', 'published_at', 'created_at',])

    def _prepare_product_tag(self, document):
        pass

    def _prepare_product_image(self, document):
        self._convert_iso_date_fields(document, ['updated_at', 'created_at',])

    def _prepare_product_variant(self, document):
        self._convert_iso_date_fields(document, ['updated_at', 'created_at',])

    def _prepare_order(self, document):
        self._convert_iso_date_fields(document, ['updated_at', 'processed_at',])

    def _prepare_customer(self, document):
        self._convert_iso_date_fields(document, ['updated_at', 'created_at',])

    def _prepare_customer_address(self, document):
        pass
