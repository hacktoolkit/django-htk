# Shopify_Lib

## Classes
- **`ShopifyProduct`** (shopify_lib/models.py) - https://help.shopify.com/api/reference/product
- **`ShopifyProductImage`** (shopify_lib/models.py) - https://help.shopify.com/api/reference/product_image
- **`ShopifyProductVariant`** (shopify_lib/models.py) - https://help.shopify.com/api/reference/product_variant
- **`ShopifyCustomer`** (shopify_lib/models.py) - https://help.shopify.com/api/reference/customer
- **`ShopifyCustomerAddress`** (shopify_lib/models.py) - https://help.shopify.com/api/reference/customeraddress
- **`ShopifyOrder`** (shopify_lib/models.py) - https://help.shopify.com/api/reference/order
- **`ShopifyFulFillment`** (shopify_lib/models.py) - https://help.shopify.com/api/reference/fulfillment
- **`ShopifyRefund`** (shopify_lib/models.py) - https://help.shopify.com/api/reference/refund
- **`ShopifyTransaction`** (shopify_lib/models.py) - https://help.shopify.com/api/reference/transaction

## Functions
- **`resource_iterator`** (shopify_lib/api.py) - Returns an iterator/generator over the ActiveResource `resource`
- **`iter_products`** (shopify_lib/api.py) - Returns an iterator/generator over all Products
- **`iter_orders`** (shopify_lib/api.py) - Returns an iterator/generator over all Orders
- **`iter_customers`** (shopify_lib/api.py) - Returns an iterator/generator over all Customers
- **`already_cached`** (shopify_lib/archivers.py) - Check whether an `item` of `item_type` was already cached
- **`archive_all`** (shopify_lib/archivers.py) - Archives everything
- **`archive_item_type`** (shopify_lib/archivers.py) - Archives a collection of Shopify.Resource of `item_type` using `iterator`
- **`archive_item`** (shopify_lib/archivers.py) - Archives a single Shopify.Resource `item` into some database using `archiver`
