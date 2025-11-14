# Caching Framework

Utilities for caching objects and managing cache lifecycles.

## Overview

The `cache` module provides:

- Abstract base classes for cacheable objects
- Locking mechanisms to prevent cache stampedes
- Configurable cache key generation
- Automatic cache invalidation via signals

## Core Concepts

### CacheableObject

Base class for objects that should be cached:

```python
from htk.cache.classes import CacheableObject

class UserFollowingCache(CacheableObject):
    def __init__(self, user):
        self.user = user

    def get_cache_key_suffix(self):
        return f'user_{self.user.id}_following'

    def get_cache_payload(self):
        # Return what to cache
        return list(self.user.following.values_list('id', flat=True))

    def get_cache_duration(self):
        # Cache for 1 hour
        return 3600
```

Usage:

```python
cache = UserFollowingCache(user)
following_ids = cache.cache_get()  # Gets from cache or recomputes
cache.invalidate_cache()  # Clear cache when user follows someone
```

### LockableObject

Prevent cache stampedes (multiple simultaneous expensive computations):

```python
from htk.cache.classes import LockableObject

class ExpensiveDataCache(LockableObject):
    def get_lock_key_suffix(self):
        return 'expensive_computation'

    def get_lock_duration(self):
        # Hold lock for 30 seconds
        return 30

    def expensive_operation(self):
        with self.lock():  # Blocks until lock is acquired
            # Expensive computation
            result = compute_something_expensive()
            return result
```

## Common Patterns

### Cache with Signal Invalidation

Automatically invalidate cache when related objects change:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=UserFollowing)
def invalidate_follower_cache(sender, instance, **kwargs):
    cache = UserFollowersCache(instance.user)
    cache.invalidate_cache()
```

### Time-Based Cache Expiration

Override `get_cache_duration()` to control TTL:

```python
class HourlyCache(CacheableObject):
    def get_cache_duration(self):
        return 3600  # 1 hour

class DailyCache(CacheableObject):
    def get_cache_duration(self):
        return 86400  # 1 day
```

### Custom Cache Key Generation

Customize cache key structure:

```python
class CustomKeyCache(CacheableObject):
    def get_cache_key(self):
        # Override for special key formatting
        suffix = self.get_cache_key_suffix()
        return f'custom:v2:{suffix}'
```

## Classes

- **`CacheableObject`** - Abstract base for cacheable objects with automatic TTL
- **`LockableObject`** - Prevent concurrent computations (cache stampede prevention)
- **`CustomCacheScheme`** - Define custom cache behavior

## Functions

- **`cache_store`** - Store data in cache
- **`cache_get`** - Retrieve data from cache
- **`invalidate_cache`** - Clear cache for an object
- **`lock`/`unlock`** - Acquire/release locks for concurrent access
- **`acquire`/`release`** - Aliases for lock/unlock

## Best Practices

1. **Use meaningful cache key suffixes** - Include relevant object IDs
2. **Set appropriate TTLs** - Balance freshness vs. performance
3. **Use locks for expensive operations** - Prevent cache stampedes
4. **Invalidate on model changes** - Use Django signals
5. **Test cache effectiveness** - Monitor hit rates in production
