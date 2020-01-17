# Python Standard Library Imports
import json
import time
from decimal import Decimal

# Third Party (PyPI) Imports
import rollbar

# HTK Imports
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

    def _reset_cache(self):
        self.items_seen = {
            # products
            'product' : {},
            'product_tag' : {},
            'product_image' : {},
            'product_variant' : {},
            # customer
            'customer' : {},
            'customer_address' : {},
            # order, refunds, fulfillments, transactions
            'order' : {},
            'order_line_item' : {},
            'fulfillment' : {},
            'refund' : {},
            'transaction' : {},
        }

    def archive_all(self, include_products=True, include_customers=True, include_orders=True):
        """Archives everything
        """
        self._reset_cache()

        if include_products:
            self._safe_archive(self.archive_products)
        if include_customers:
            self._safe_archive(self.archive_customers)
        if include_orders:
            self._safe_archive(self.archive_orders)

    def _safe_archive(self, archiver):
        """Safely executes archival of Shopify resources using `archiver`

        Disables foreign key checks before start of archival, and reenables after
        """
        from htk.utils.db import disable_foreign_key_checks
        from htk.utils.db import enable_foreign_key_checks

        try:
            disable_foreign_key_checks()
            archiver()
        except:
            rollbar.report_exc_info()
        finally:
            enable_foreign_key_checks()

    @CachedAttribute
    def fk_item_types(self):
        item_types = (
            # product-related
            'product_tag',
            'product_image',
            'product_variant',
            # customer-related
            'customer_address',
            # order-related
            'order_line_item',
            'fulfillment',
            'refund',
            'transaction',
        )
        return item_types

    def archive_products(self):
        self.archive_item_type('product')

    def archive_orders(self):
        self.archive_item_type('order')

    def archive_customers(self):
        self.archive_item_type('customer')

    def archive_item_type(self, item_type):
        """Archives a collection of Shopify.Resource of `item_type` using `iterator`
        """
        start_time = time.time()
        msg = 'Archiving %ss...' % item_type
        print(msg)
        slack_notifications_enabled = htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED')
        if slack_notifications_enabled:
            from htk.utils.notifications import slack_notify
            slack_notify(msg)

        num_archived = 0
        iterator = self._get_iterator_for_item_type(item_type)
        for item, i, total, page in iterator():
            msg =  '%s of %s %ss'  % (i, total, item_type,)
            print(msg)
            self.archive_item(item_type, item)
            num_archived = i

        if slack_notifications_enabled:
            from htk.utils.notifications import slack_notify
            end_time = time.time()
            duration = Decimal(end_time - start_time).quantize(Decimal(10) ** -2)
            msg = 'Archived %s %ss in %s seconds' % (num_archived, item_type, duration,)
            slack_notify(msg)

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
            self.mongodb_connection = htk_setting('HTK_MONGODB_CONNECTION')
        else:
            self.mongodb_connection = mongodb_connection
        if mongodb_name is None:
            self.mongodb_name = htk_setting('HTK_MONGODB_NAME')
        else:
            self.mongodb_name = mongodb_name

        self.mongodb_initialized = False
        super(HtkShopifyMongoDBArchiver, self).__init__(api=api)

    def get_collection_name(self, item_type):
        collections = htk_setting('HTK_SHOPIFY_MONGODB_COLLECTIONS')
        collection_name = collections[item_type]
        return collection_name

    def _init_mongodb(self):
        if not self.mongodb_initialized:
            from pymongo import MongoClient
            self.mongo_client = MongoClient(self.mongodb_connection)
            self.mongo_db = self.mongo_client[self.mongodb_name]
            self.mongodb_initialized = True

    def _get_document_preparator(self, item_type):
        preparators = {
            # products
            'product' : self._prepare_product,
            'product_tag' : self._prepare_product_tag,
            'product_image' : self._prepare_product_image,
            'product_variant' : self._prepare_product_variant,
            # customers
            'customer' : self._prepare_customer,
            'customer_address' : self._prepare_customer_address,
            # orders, refunds, fulfillments, transactions
            'order' : self._prepare_order,
            'order_line_item' : self._prepare_order_line_item,
            'fulfillment' : self._prepare_fulfillment,
            'refund' : self._prepare_refund,
            'transaction' : self._prepare_transaction,
        }
        preparator = preparators.get(item_type)
        return preparator

    def _db_upsert(self, item_type, document, pk):
        """Performs the actual DB upsert
        """
        self._init_mongodb()

        collection_name = self.get_collection_name(item_type)
        collection = self.mongo_db[collection_name]

        collection.replace_one({ '_id' : pk, }, document, upsert=True)

    def upsert(self, item_type, document):
        key = lambda document: document['_id']
        pk = key(document)
        if self.already_cached(item_type, document, key):
            if item_type not in self.fk_item_types:
                print('Skipping duplicate processed in session {}: {}'.format(item_type, pk))
                print(document)
        else:
            preparator = self._get_document_preparator(item_type)
            if preparator:
                preparator(document)
            self._db_upsert(item_type, document, pk)

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

    ######################################################################
    # Products

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
        tags = [tag.strip().lower() for tag in tags_str.split(',')]
        for tag in tags:
            self._archive_product_tag('product_tag', tag, pk)
        document['tags'] = tags

        # rewrite images as foreign key
        product_image = document['image']
        image_id = self._archive_product_image('product_image', product_image, pk)
        document['image_id'] = image_id
        del document['image']
        # images -> image_ids (fk)
        image_ids = [self._archive_product_image('product_image', product_image, pk) for product_image in document.get('images', [])]
        document['image_ids'] = image_ids
        del document['images']

        # rewrite variants as foreign key
        variant_ids = [self._archive_product_variant('product_variant', product_variant, pk) for product_variant in document.get('variants', [])]
        document['variant_ids'] = variant_ids
        del document['variants']
        variant_id = variant_ids[0] if len(variant_ids) else None
        document['variant_id'] = variant_id

        self.upsert(item_type, document)
        return pk

    def _archive_product_tag(self, item_type, tag, product_id):
        document = {
            '_id' : tag,
        }

        self.upsert(item_type, document)
        return tag

    def _archive_product_image(self, item_type, document, product_id):
        pk = document['id']
        document['_id'] = pk
        del document['id']
        document['product_id'] = product_id

        self.upsert(item_type, document)
        return pk

    def _archive_product_variant(self, item_type, document, product_id):
        pk = document['id']
        document['_id'] = pk
        del document['id']
        document['product_id'] = product_id

        self.upsert(item_type, document)
        return pk

    ######################################################################
    # Customers

    def archive_customer(self, item_type, customer):
        document = json.loads(customer.to_json())[item_type]
        pk = document['id']
        document['_id'] = pk
        del document['id']

        # rewrite tags as array
        tags_str = document['tags']
        tags = [tag.strip().lower() for tag in tags_str.split(',')]
        # TODO
        # for tag in tags:
        #     self._archive_customer_tag('customer_tag', tag)
        document['tags'] = tags

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

    ######################################################################
    # Orders

    def archive_order(self, item_type, order):
        document = json.loads(order.to_json())[item_type]
        pk = document['id']
        document['_id'] = pk
        del document['id']

        # rewrite line_items as foreign key
        line_item_ids = [self._archive_order_line_item('order_line_item', order_line_item, pk) for order_line_item in document.get('line_items', [])]
        document['line_item_ids'] = line_item_ids
        del document['line_items']

        # rewrite fulfillments as foreign key
        fulfillment_ids = [self._archive_fulfillment('fulfillment', fulfillment, pk) for fulfillment in document.get('fulfillments', [])]
        document['fulfillment_ids'] = fulfillment_ids
        del document['fulfillments']

        # rewrite refunds as foreign key
        refund_ids = [self._archive_refund('refund', refund, pk) for refund in document.get('refunds', [])]
        document['refund_ids'] = refund_ids
        if 'refunds' in document:
            del document['refunds']

        # rewrite tags as array
        tags_str = document['tags']
        tags = [tag.strip().lower() for tag in tags_str.split(',')]
        # TODO
        # for tag in tags:
        #     self._archive_order_tag('order_tag', tag)
        document['tags'] = tags

        # rewrite customer as foreign key
        customer_id = document['customer']['id']
        document['customer_id'] = customer_id
        del document['customer']

        self.upsert(item_type, document)
        return pk

    def _archive_order_line_item(self, item_type, document, order_id):
        pk = document['id']
        del document['id']
        document['_id'] = pk
        document['order_id'] = order_id

        self.upsert(item_type, document)
        return pk

    def _archive_fulfillment(self, item_type, document, order_id):
        pk = document['id']
        del document['id']
        document['_id'] = pk
        document['order_id'] = order_id

        self.upsert(item_type, document)
        return pk

    def _archive_refund(self, item_type, document, order_id):
        pk = document['id']
        del document['id']
        document['_id'] = pk
        document['order_id'] = order_id

        # rewrite transactions as foreign key
        transaction_ids = [self._archive_transaction('transaction', transaction, order_id, refund_id=pk) for transaction in document.get('transactions', [])]
        document['transaction_ids'] = transaction_ids
        del document['transactions']

        # enforce boolean
        document['restock'] = bool(document.get('restock'))

        self.upsert(item_type, document)
        return pk

    def _archive_transaction(self, item_type, document, order_id, refund_id=None):
        pk = document['id']
        del document['id']
        document['_id'] = pk
        document['order_id'] = order_id
        document['refund_id'] = refund_id

        self.upsert(item_type, document)
        return pk

    ######################################################################
    # Preparation methods

    def _prepare_product(self, document):
        self._convert_iso_date_fields(document, ['created_at', 'updated_at', 'published_at',])

    def _prepare_product_tag(self, document):
        pass

    def _prepare_product_image(self, document):
        self._convert_iso_date_fields(document, ['created_at', 'updated_at',])

    def _prepare_product_variant(self, document):
        self._convert_iso_date_fields(document, ['created_at', 'updated_at',])

    def _prepare_customer(self, document):
        self._convert_iso_date_fields(document, ['created_at', 'updated_at',])

    def _prepare_customer_address(self, document):
        pass

    def _prepare_order(self, document):
        self._convert_iso_date_fields(document, ['created_at', 'updated_at',])

    def _prepare_order_line_item(self, document):
        pass

    def _prepare_fulfillment(self, document):
        self._convert_iso_date_fields(document, ['created_at', 'updated_at',])

    def _prepare_refund(self, document):
        self._convert_iso_date_fields(document, ['created_at', 'processed_at',])

    def _prepare_transaction(self, document):
        self._convert_iso_date_fields(document, ['created_at',])

class HtkShopifySQLArchiver(HtkShopifyMongoDBArchiver):
    def __init__(self, mongodb_dual_archive=False):
        self.mongodb_dual_archive = mongodb_dual_archive
        super(HtkShopifySQLArchiver, self).__init__()

    def get_model(self, item_type):
        models = htk_setting('HTK_SHOPIFY_SQL_MODELS')

        model_cls = models[item_type]
        from htk.utils import resolve_model_dynamically
        model = resolve_model_dynamically(model_cls)
        return model

    def _db_upsert(self, item_type, document, pk):
        """Performs the actual DB upsert

        Convert a MongoDB `document` of `item_type` into a Django model instance and upsert it
        """
        if self.mongodb_dual_archive:
            try:
                super(HtkShopifySQLArchiver, self)._db_upsert(item_type, document, pk)
            except:
                rollbar.report_exc_info()

        model = self.get_model(item_type)
        instance = model.from_document(document)
        persisted_instance = instance.upsert()
        return persisted_instance
