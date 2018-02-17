import math
import shopify
import time

SHOPIFY_API_RATE_LIMIT_CYCLE = 0.5 # can average 2 calls per second

class HtkShopifyAPIClient(object):
    def __init__(self, shop_name=None, api_key=None, api_secret=None):
        self.shop_name = shop_name
        self.api_key = api_key
        self.api_secret = api_secret

        self.reset_session()

    def reset_session(self):
        shopify.ShopifyResource.clear_session()
        if self.shop_name and self.api_key and self.api_secret:
            shop_url = 'https://%s:%s@%s.myshopify.com/admin' % (self.api_key, self.api_secret, self.shop_name,)
            shopify.ShopifyResource.set_site(shop_url)
            self.shop = shopify.Shop.current()
        else:
            self.shop = None
            raise Exception('Missing Shopify store or API parameters')

    def resource_iterator(self, resource):
        """Returns an iterator/generator over the ActiveResource `resource`
        """
        item_count = resource.count()
        page_size = 250
        num_pages = int(math.ceil(item_count / (page_size * 1.0)))

        i = 0
        start_time = time.time()
        for page in xrange(1, num_pages + 1):
            if page > 1:
                # implement leaky bucket to avoid 429 TOO MANY REQUESTS
                stop_time = time.time()
                processing_duration = stop_time - start_time
                wait_time = int(math.ceil(SHOPIFY_API_RATE_LIMIT_CYCLE - processing_duration))
                if wait_time > 0:
                    time.sleep(wait_time)

            items = resource.find(limit=page_size, page=page)
            for item in items:
                i += 1
                yield item, i, item_count, page

    ##
    # Product
    # https://help.shopify.com/api/reference/product

    def iter_products(self):
        """Returns an iterator/generator over all Products
        """
        return self.resource_iterator(shopify.Product)

    ##
    # Order
    # https://help.shopify.com/api/reference/order

    def iter_orders(self):
        """Returns an iterator/generator over all Orders
        """
        return self.resource_iterator(shopify.Order)

    ##
    # Customer
    # https://help.shopify.com/api/reference/customer

    def iter_customers(self):
        """Returns an iterator/generator over all Customers
        """
        return self.resource_iterator(shopify.Customer)
