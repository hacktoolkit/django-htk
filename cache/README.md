# Cache

## Classes
- **`CacheableObject`** (cache/classes.py) - Abstract base class for cacheable objects
- **`LockableObject`** (cache/classes.py) - Abstract base class for lockable objects
- **`CustomCacheScheme`** (cache/classes.py) - Abstract base class for custom cache schemes

## Functions
- **`get_cache_payload`** (cache/classes.py) - Default payload
- **`get_cache_duration`** (cache/classes.py) - Default cache duration in seconds
- **`get_cache_key_suffix`** (cache/classes.py) - Default cache key suffix
- **`get_cache_key`** (cache/classes.py) - Default cache key
- **`invalidate_cache`** (cache/classes.py) - Default cache invalidation method
- **`cache_store`** (cache/classes.py) - Default cache store method
- **`get_lock_duration`** (cache/classes.py) - Default lock duration in seconds
- **`get_lock_key_suffix`** (cache/classes.py) - Default lock key suffix
- **`get_lock_key`** (cache/classes.py) - Default lock key
- **`acquire`** (cache/classes.py) - Alias for lock()
- **`release`** (cache/classes.py) - Alias for unlock()
- **`lock`** (cache/classes.py) - Lock an object, blocking concurrent access
- **`unlock`** (cache/classes.py) - Unlock the object for concurrent access
- **`get_cache_key_suffix`** (cache/classes.py) - Cache key suffix based on the prekey
- **`get_cache_key`** (cache/classes.py) - Default cache key
- **`get_cache_payload`** (cache/classes.py) - Default payload
- **`invalidate_cacheable_object`** (cache/signal_hooks.py) - Generic receiver for CacheableObjects
- **`refresh_cacheable_object`** (cache/signal_hooks.py) - Generic receiver for CacheableObjects
