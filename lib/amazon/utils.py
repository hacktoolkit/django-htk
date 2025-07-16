# Python Standard Library Imports
import re
import typing as T

# Third Party (PyPI) Imports
import requests
from bs4 import BeautifulSoup


def build_amazon_product_url(product_id: str) -> str:
    url = f"https://www.amazon.com/dp/{product_id}"
    return url


def extract_asin_from_amazon_product_url(
    product_id: str, headers: T.Optional[dict[str, str]] = None
) -> str:
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; HacktoolkitBot/1.0; +https://hacktoolkit.com)",
            "Accept-Language": "en-US,en;q=0.9",
        }

    url = build_amazon_product_url(product_id)

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Try structured data first
    asin = None
    asin_input = soup.find("input", {"id": "ASIN"})
    if asin_input and asin_input.get("value"):
        asin = asin_input["value"].strip()
    else:
        # Fallback: look in detail bullets
        detail_bullets = soup.find(id="detailBullets_feature_div")
        if detail_bullets:
            text = detail_bullets.get_text()
            match = re.search(r"ASIN\s*:\s*([A-Z0-9]{10})", text)
            if match:
                asin = match.group(1).strip()

    if not asin:
        raise ValueError("ASIN not found in product page")

    return asin


def build_amazon_ad_image_url(product_id: str, tag: str) -> str:
    url = f'http://ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN={product_id}&Format=_SL250_&ID=AsinImage&MarketPlace=US&ServiceVersion=20070822&WS=1&tag={tag}'
    return url


def build_amazon_media_image_url(
    asin: str, size_suffix: str = "_SL1500_"
) -> str:
    """Constructs a static Amazon product image URL based on the ASIN and desired image size.

    Note:
        This method assumes the product image hash matches the ASIN, which may not hold true
        for many products. It works reliably only when Amazon uses the ASIN as the image filename.
        For guaranteed accuracy, use a scraping method or the Product Advertising API to obtain
        the correct image hash.

    Args:
        asin (str): The 10-character Amazon Standard Identification Number (ASIN) of the product.
        size_suffix (str): Optional size modifier appended to the image filename. Common suffixes include:

            - "_SL1500_"  → Scaled longest side to 1500px (default)
            - "_SL1000_"  → Scaled longest side to 1000px
            - "_SX300_"   → Scaled width to 300px
            - "_SX500_"   → Scaled width to 500px
            - "_SY400_"   → Scaled height to 400px
            - "_SS100_"   → Square 100x100px
            - "_AC_"      → Auto-configured size (Amazon's default responsive image mode)

    Returns:
        str: The full CDN URL pointing to the image of the given product, using the provided ASIN and size.

    Example:
    >>> get_amazon_image_url("B0C5JP7HN7", "_SX500_")
    'https://m.media-amazon.com/images/I/B0C5JP7HN7._SX500_.jpg'

    >>> get_amazon_image_url("B0C5JP7HN7")
    'https://m.media-amazon.com/images/I/B0C5JP7HN7._SL1500_.jpg'
    """
    url = f"https://m.media-amazon.com/images/I/{asin}.{size_suffix}.jpg"
    return url
