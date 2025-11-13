# Amazon Integration

Amazon product utilities and image URLs.

## Quick Start

```python
from htk.lib.amazon.utils import build_amazon_media_image_url

# Generate product image URL from ASIN
image_url = build_amazon_media_image_url(asin='B00EXAMPLE', size='large')
```

## Configuration

```python
# settings.py
AMAZON_ASSOCIATE_TAG = os.environ.get('AMAZON_ASSOCIATE_TAG')
```

## Related Modules

- `htk.lib.shopify_lib` - E-commerce integrations
