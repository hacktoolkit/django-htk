# Shopify Library Constants

Configuration constants for Shopify API integration.

## Configuration Settings

```python
from htk.lib.shopify_lib.constants import (
    HTK_SHOPIFY_SHOP_NAME,
    HTK_SHOPIFY_API_KEY,
    HTK_SHOPIFY_API_SECRET,
    HTK_SHOPIFY_SHARED_SECRET,
    HTK_SHOPIFY_MONGODB_COLLECTIONS,
    HTK_SHOPIFY_MONGODB_ITEM_PK,
    HTK_SHOPIFY_SQL_MODELS,
)
```

## API Authentication

Configure Shopify API credentials in Django settings:

```python
# settings.py
HTK_SHOPIFY_SHOP_NAME = 'your-shop-name'
HTK_SHOPIFY_API_KEY = 'your-api-key'
HTK_SHOPIFY_API_SECRET = 'your-api-secret'
HTK_SHOPIFY_SHARED_SECRET = 'your-shared-secret'
```

## MongoDB Collections

Map Shopify object types to MongoDB collections:

```python
HTK_SHOPIFY_MONGODB_COLLECTIONS = {
    'product': 'product',
    'product_tag': 'product_tag',
    'product_image': 'product_image',
    'product_variant': 'product_variant',
    'customer': 'customer',
    'customer_address': 'customer_address',
    'order': 'order',
    'order_line_item': 'order_line_item',
    'fulfillment': 'fulfillment',
    'refund': 'refund',
    'transaction': 'transaction',
}
```

## SQL Models

Map Shopify object types to Django model paths:

```python
HTK_SHOPIFY_SQL_MODELS = {
    'product': 'shopify.ShopifyProduct',
    'product_variant': 'shopify.ShopifyProductVariant',
    'customer': 'shopify.ShopifyCustomer',
    'order': 'shopify.ShopifyOrder',
}
```
