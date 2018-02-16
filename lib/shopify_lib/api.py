import rollbar
import shopify

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

    ##
    # Product
    # https://help.shopify.com/api/reference/product

    def get_all_products(self):
        products = shopify.Product.find()
        return products
