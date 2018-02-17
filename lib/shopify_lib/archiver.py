import json

from htk.utils import htk_setting

class HtkShopifyArchiver(object):
    def __init__(self, api=None):
        if api is None:
            from htk.lib.shopify_lib.utils import get_shopify_api_cli
            api = get_shopify_api_cli()
        self.api = api

    def archive_all(self):
        self.archive_products()
        self.archive_orders()
        self.archive_customers()

    def archive_products(self):
        for product in self.api.iter_products():
            self.archive_item('product', product)

    def archive_orders(self):
        for order in self.api.iter_orders():
            self.archive_item('order', order)

    def archive_customers(self):
        for customer in self.api.iter_customers():
            self.archive_item('customer', customer)

    def archive_item(self, item_type, item):
        """Archives a Shopify.Resource item into some database
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
            item_id = item_json['id']
            # set the primary key
            item_json['_id'] = item_id
            del item_json['id']
            collection.insert(item_json)
