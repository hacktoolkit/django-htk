# KV Storage App

Key-value storage for flexible, schema-less data storage.

## Overview

The `kv_storage` app provides:

- Simple key-value storage backed by the database
- Flexible schema without migrations
- JSON value support
- Caching for performance
- Thread-safe operations

## Quick Start

### Store & Retrieve Data

```python
from htk.apps.kv_storage.utils import kv_put, kv_get

# Store a value
kv_put('user_preferences', {'theme': 'dark', 'notifications': True})

# Retrieve a value
prefs = kv_get('user_preferences')
# {'theme': 'dark', 'notifications': True}

# Get with default
kv_get('nonexistent_key', default={})
```

### Delete Values

```python
from htk.apps.kv_storage.utils import kv_delete

# Delete a key
kv_delete('user_preferences')

# Check if exists before deleting
if kv_get('key'):
    kv_delete('key')
```

### Cached Access

```python
from htk.apps.kv_storage.utils import kv_get_cached

# Get value from cache (fetches from DB if not cached)
value = kv_get_cached('expensive_setting')

# Cached values auto-refresh based on TTL
```

## Models

- **`AbstractKVStorage`** - Extend this for custom storage models

Create a custom model in your app:

```python
from htk.apps.kv_storage.models import AbstractKVStorage

class AppConfig(AbstractKVStorage):
    class Meta:
        db_table = 'app_config'
```

## Common Patterns

### User Settings

```python
# Store per-user settings
user_id = user.id
kv_put(f'user_settings:{user_id}', {
    'language': 'en',
    'timezone': 'America/New_York',
    'email_digest': 'daily'
})

# Retrieve user settings
settings = kv_get(f'user_settings:{user_id}')
```

### Feature Configuration

```python
# Store feature settings without migrations
kv_put('feature:analytics_config', {
    'sampling_rate': 0.1,
    'retention_days': 90,
    'debug': False
})

config = kv_get('feature:analytics_config')
```

### Application State

```python
# Store transient application state
kv_put('background_job:sync_users:status', {
    'last_run': '2024-11-13T15:30:00Z',
    'processed': 1243,
    'failed': 0,
    'next_run': '2024-11-13T16:00:00Z'
})

status = kv_get('background_job:sync_users:status')
```

### Caching Complex Data

```python
from htk.apps.kv_storage.utils import kv_put, kv_get_cached

# Expensive operation - store result
data = expensive_computation()
kv_put('expensive_result', data)

# Later - retrieve from cache
cached_data = kv_get_cached('expensive_result')
```

## Naming Conventions

Use descriptive, hierarchical keys:

```python
# Good
'user_settings:1234'
'feature:dark_mode:config'
'cache:homepage:data'
'state:import_job:123'

# Avoid
'data'
'tmp'
'x'
```

## Best Practices

1. **Use hierarchical keys** - `namespace:subnamespace:key`
2. **Store JSON data** - Complex values as dictionaries
3. **Cache expensive data** - Compute once, store, retrieve many times
4. **Set reasonable TTLs** - Don't cache indefinitely
5. **Document keys** - Explain what each key stores
6. **Clean up old keys** - Periodically purge unused data
7. **Use atomic operations** - Avoid race conditions

## Performance

```python
# Slow - multiple DB hits
for user in users:
    prefs = kv_get(f'user_prefs:{user.id}')  # Each hit DB

# Better - batch get
from htk.apps.kv_storage.models import get_kv_storage_model
KVStorage = get_kv_storage_model()
all_keys = [f'user_prefs:{u.id}' for u in users]
prefs_dict = {k.key: k.value for k in KVStorage.objects.filter(key__in=all_keys)}
```

## Related Modules

- `htk.cache` - For more complex caching
- `htk.utils` - General utilities
