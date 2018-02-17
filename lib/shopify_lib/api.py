import rollbar
import shopify
import time

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
        count = resource.count()
        page_size = 50
        has_remainder = count % page_size
        num_pages = (count / page_size) + (1 if has_remainder else 0)
        for page in xrange(num_pages):
            items = resource.find(page=page)
            for item in items:
                yield item
            time.sleep(1)

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
