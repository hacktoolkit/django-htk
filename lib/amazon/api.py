# Third Party (PyPI) Imports
from amazon_paapi import AmazonApi

# HTK Imports
from htk.utils import htk_setting


def get_amazon_pa_api():
    amazon = AmazonApi(
        key=htk_setting('HTK_AMAZON_PRODUCT_ADVERTISING_API_ACCESS_KEY'),
        secret=htk_setting('HTK_AMAZON_PRODUCT_ADVERTISING_API_SECRET_KEY'),
        tag=htk_setting('HTK_AMAZON_TRACKING_ID'),
        country="US",
    )
    return amazon


def get_amazon_product_image_url(product_id: str) -> str:
    amazon = get_amazon_pa_api()
    items = amazon.get_items([product_id])
    # for item in items:
    #     print("Title:", item.title)
    #     print("Image URL:", item.images.large)
    #     print("ASIN:", item.asin)
    #     print("Price:", item.prices.current_price)

    image_url = items[0].images.large
    return image_url
