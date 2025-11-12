# HTK Cache Module

> Flexible caching system with customizable cache keys, timeouts, and signal-based invalidation.

## Purpose

The cache module extends Django's caching framework with mixin-based caching. Objects become cacheable through inheritance, with custom cache keys, configurable timeouts, and automatic invalidation via signals.

## Quick Start

```python
from django.db import models
from htk.cache.classes import CacheableObject
from htk.constants.time import TIMEOUT_1_HOUR

class Product(models.Model, CacheableObject):
    """Django model that is also cacheable"""
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_cache_key_suffix(self):
        return self.id

    def get_cache_duration(self):
        return TIMEOUT_1_HOUR

# Use it
product = Product.objects.get(id=1)
cached = product.cache_get()  # Get from cache
product.cache_set()  # Store in cache
product.cache_delete()  # Remove from cache
```

## Key Components

| Component | Purpose |
|-----------|---------|
| **CacheableObject** | Mixin class for any object to become cacheable |
| **CustomCacheScheme** | Flexible cache key generation with namespacing |
| **LockableObject** | Thread-safe caching preventing cache stampede |
| **Cache signals** | `invalidate_cacheable_object`, `refresh_cacheable_object` |

## Common Patterns

### Model Caching

```python
from django.db import models
from htk.cache.classes import CacheableObject

class Author(models.Model, CacheableObject):
    name = models.CharField(max_length=255)

    def get_books(self):
        """Cache list of books for this author"""
        cache_key = f'author_{self.id}_books'
        books = cache.get(cache_key)

        if books is None:
            books = list(self.book_set.all())
            cache.set(cache_key, books, TIMEOUT_1_DAY)

        return books
```

### Cache Invalidation with Signals

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from htk.cache.signal_hooks import invalidate_cacheable_object

@receiver(post_save, sender=BlogPost)
def invalidate_post_cache(sender, instance, **kwargs):
    """Invalidate cache when post is saved"""
    invalidate_cacheable_object.send(sender=BlogPost, instance=instance)
```

### Custom Cache Keys

```python
from htk.cache.classes import CustomCacheScheme

cache_scheme = CustomCacheScheme(
    prefix='myapp',
    namespace='products',
    key_parts=['category', 'id']
)

# Generates: 'myapp:products:electronics:123'
cache_key = cache_scheme.get_key(category='electronics', id=123)
```

### View Caching

```python
from django.views import View
from django.core.cache import cache
from htk.constants.time import TIMEOUT_1_HOUR

class ProductDetailView(View):
    def get(self, request, product_id):
        cache_key = f'product_{product_id}'
        product = cache.get(cache_key)

        if product is None:
            product = Product.objects.get(id=product_id)
            cache.set(cache_key, product, TIMEOUT_1_HOUR)

        return render(request, 'product.html', {'product': product})
```

## Time Constants

Available from `htk.constants.time`:

| Constant | Value |
|----------|-------|
| `TIMEOUT_1_MINUTE` | 60 seconds |
| `TIMEOUT_5_MINUTES` | 300 seconds |
| `TIMEOUT_30_MINUTES` | 1800 seconds |
| `TIMEOUT_1_HOUR` | 3600 seconds |
| `TIMEOUT_1_DAY` | 86400 seconds |
| `TIMEOUT_1_WEEK` | 604800 seconds |
| `TIMEOUT_NONE` | None (cache forever) |

## Configuration

Django's caching backend must be configured:

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

## Best Practices

- **Use appropriate timeouts** - 5-10 min for short-lived, 1 hour for medium, 1 day for long-lived
- **Invalidate strategically** - Delete specific cache keys, not entire cache
- **Use signals for auto-invalidation** - Wire Django signals to cache removal on model changes
- **Use LockableObject** - Prevents cache stampede for expensive operations
- **Include versions** - Add version numbers to cache keys for easy invalidation

## Testing

```python
from django.test import TestCase
from django.core.cache import cache

class CacheTestCase(TestCase):
    def test_product_caching(self):
        """Test product caching."""
        product = Product.objects.create(name='Widget', price=99)

        # First access loads from DB
        product.cache_set()
        cached = cache.get(product.get_cache_key())
        self.assertEqual(cached.id, product.id)

        # Second access hits cache
        product_from_cache = cache.get(product.get_cache_key())
        self.assertIsNotNone(product_from_cache)
```

## API Reference

| Method | Purpose |
|--------|---------|
| `get_cache_payload()` | Return object to cache (default: self) |
| `get_cache_duration()` | Return timeout in seconds |
| `get_cache_key_suffix()` | Return cache key suffix |
| `get_cache_key()` | Return full cache key |
| `cache_get()` | Retrieve from cache |
| `cache_set()` | Store in cache |
| `cache_delete()` | Remove from cache |
| `cache_refresh()` | Refresh cache |

## Related Modules

- `htk.cache.classes` - CacheableObject and CustomCacheScheme
- `htk.cache.signal_hooks` - Invalidation signals
- `htk.constants.time` - Time constants
- `htk.utils.cache_descriptors` - Cached property decorators

## References

- [Django Cache Framework](https://docs.djangoproject.com/en/stable/topics/cache/)
- [Django Signals](https://docs.djangoproject.com/en/stable/topics/signals/)

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
