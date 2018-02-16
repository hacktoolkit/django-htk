from htk.utils import htk_setting

def get_shopify_api_cli(shop_name=None, api_key=None, api_secret=None):
    from htk.lib.shopify_lib.api import HtkShopifyAPIClient
    shop_name = shop_name if shop_name else htk_setting('HTK_SHOPIFY_SHOP_NAME')
    api_key = api_key if api_key else htk_setting('HTK_SHOPIFY_API_KEY')
    api_secret = api_secret if api_secret else htk_setting('HTK_SHOPIFY_API_SECRET')
    api = HtkShopifyAPIClient(shop_name=shop_name, api_key=api_key, api_secret=api_secret)
    return api
