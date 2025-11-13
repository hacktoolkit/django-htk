# Shopify Integration

E-commerce API for products, orders, customers, and fulfillment.

## Quick Start

```python
from htk.lib.shopify_lib.api import iter_products, iter_orders, iter_customers

# Iterate products
for product in iter_products():
    print(product.title, product.handle)

# Iterate orders
for order in iter_orders():
    print(order.id, order.total_price)

# Iterate customers
for customer in iter_customers():
    print(customer.email, customer.first_name)
```

## Models

- **`ShopifyProduct`** - Product with variants and images
- **`ShopifyOrder`** - Order with fulfillments
- **`ShopifyCustomer`** - Customer with addresses
- **`ShopifyFulfillment`** - Order fulfillment
- **`ShopifyTransaction`** - Payment transaction

## Archiving

```python
from htk.lib.shopify_lib.archivers import archive_all, archive_item_type

# Archive all data from Shopify
archive_all()

# Archive specific type
archive_item_type('Product')
```

## Configuration

```python
# settings.py
SHOPIFY_STORE_NAME = os.environ.get('SHOPIFY_STORE_NAME')
SHOPIFY_API_KEY = os.environ.get('SHOPIFY_API_KEY')
SHOPIFY_API_PASSWORD = os.environ.get('SHOPIFY_API_PASSWORD')
```

## Related Modules

- `htk.apps.store` - Store management
- `htk.apps.customers` - Customer management
