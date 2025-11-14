# Store Constants

## Overview

This module defines configuration for the e-commerce store system, including product and collection model references.

## Constants

### Model References

- **`HTK_STORE_PRODUCT_MODEL`** - Default: `None` - Product model (app_label.ModelName)
- **`HTK_STORE_PRODUCT_COLLECTION_MODEL`** - Default: `None` - Product collection/category model

## Usage Examples

### Configure Store Models

```python
# In Django settings.py
HTK_STORE_PRODUCT_MODEL = 'store.Product'
HTK_STORE_PRODUCT_COLLECTION_MODEL = 'store.Collection'
```

### Load Models Dynamically

```python
from django.apps import apps
from htk.apps.store.constants import (
    HTK_STORE_PRODUCT_MODEL,
    HTK_STORE_PRODUCT_COLLECTION_MODEL,
)

Product = apps.get_model(HTK_STORE_PRODUCT_MODEL)
Collection = apps.get_model(HTK_STORE_PRODUCT_COLLECTION_MODEL)

products = Product.objects.all()
collections = Collection.objects.all()
```

### Use in Queries

```python
from django.apps import apps
from htk.apps.store.constants import HTK_STORE_PRODUCT_MODEL

Product = apps.get_model(HTK_STORE_PRODUCT_MODEL)
featured = Product.objects.filter(featured=True)
```
