# Cache Constants

> Cache key prefix configuration for HTK caching system

## Purpose
This module provides cache-related constants, primarily the default cache key prefix used throughout the HTK framework to namespace cached data and avoid key collisions.

## Key Files
- `__init__.py` - Empty or minimal imports
- `defaults.py` - Default cache configuration values

## Key Components / Features

### Cache Key Prefix (`defaults.py`)
- `HTK_CACHE_KEY_PREFIX` - Default prefix for all HTK cache keys (default: 'htk')

## Usage

```python
from htk.cache.constants import HTK_CACHE_KEY_PREFIX
from django.core.cache import cache

# Build namespaced cache key
def get_cache_key(key_suffix):
    return f"{HTK_CACHE_KEY_PREFIX}:{key_suffix}"

# Store data in cache
cache_key = get_cache_key('user:123:profile')
cache.set(cache_key, user_profile_data, timeout=3600)

# Retrieve from cache
cached_data = cache.get(cache_key)

# Delete cache with pattern
cache_pattern = f"{HTK_CACHE_KEY_PREFIX}:user:*"
# Use pattern matching to invalidate related keys
```

## Related Modules
- Parent: `htk/cache/`
- Related:
  - `htk.cache.utils` - Cache utility functions using this prefix
  - `htk.utils.cache_descriptors` - Cache decorators and descriptors

## Notes
- Confidence: HIGH (>98%)
- Last Updated: November 2025
- Can be overridden in Django settings to customize cache namespace
- Prevents cache key collisions in multi-tenant or shared cache environments
