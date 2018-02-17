import json

from htk.utils import htk_setting

class HtkShopifyArchiver(object):
    def __init__(self, api=None):
        if api is None:
            from htk.lib.shopify_lib.utils import get_shopify_api_cli
            api = get_shopify_api_cli()
        self.api = api

    def archive_all(self):
        self.items_seen = {
            'product' : {},
            'order' : {},
            'customer' : {},
        }
        self.archive_products()
        self.archive_orders()
        self.archive_customers()

    def archive_item_type(self, item_type, iterator):
        """Archives a collection of Shopify.Resource of `item_type` using `iterator`
        """
        print 'Archiving %ss' % item_type
        for item, i, total, page in iterator():
            print '%s of %s %ss'  % (i, total, item_type,)
            self.archive_item(item_type, item)

    def archive_products(self):
        self.archive_item_type('product', self.api.iter_products)

    def archive_orders(self):
        self.archive_item_type('order', self.api.iter_orders)

    def archive_customers(self):
        self.archive_item_type('customer', self.api.iter_customers)

    def archive_item(self, item_type, item):
        """Archives a single Shopify.Resource item into some database
        """
        raise Exception('HtkShopifyArchiver::archive_item not implemented')

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
        collection_name = collections.get(item_type)
        return collection_name

    def archive_item(self, item_type, item):
        """Archive a Shopify.Resource item in MongoDB
        """
        collection_name = self.get_collection_name(item_type)
        if collection_name:
            collection = self.mongo_db[collection_name]

            item_json = json.loads(item.to_json())[item_type]
            # set the primary key
            get_item_pk = htk_setting('HTK_SHOPIFY_MONGODB_ITEM_PK')
            item_id = get_item_pk(item_type, item_json)
            item_json['_id'] = item_id
            if item_id == item_json['id']:
                # remove the redundant id
                del item_json['id']

            if item_id in self.items_seen[item_type]:
                print 'Skipping duplicate %s: %s' % (item_type, item_id,)
                print item_json
            else:
                self.items_seen[item_type][item_id] = True
                collection.insert(item_json)
