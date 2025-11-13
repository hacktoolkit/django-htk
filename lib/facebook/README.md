# Integration

## Overview

This integration integrates with an external service, providing a Python client and utilities for common operations.

## Quick Start

### Initialize Client

```python
from htk.lib.facebook.utils import Client

# Create client with credentials
client = Client(api_key='your_api_key')

# Or use from settings
client = Client()  # Uses HTK_FACEBOOK_API_KEY from settings
```

### Basic Operation

```python
# Get resource
resource = client.get_resource(id='resource_id')

# List resources
resources = client.list_resources(limit=10)

# Create resource
new_resource = client.create_resource(name='My Resource')
```

## Operations

### Read Operations

```python
# Get single resource
resource = client.get(id='123')

# List resources
resources = client.list(limit=10, offset=0)

# Search
results = client.search(query='search term')

# Count
count = client.count()
```

### Write Operations

```python
# Create resource
new = client.create(name='test')

# Update resource
updated = client.update(id='123', name='new name')

# Delete resource
client.delete(id='123')
```

## Authentication

Configure credentials:

```python
# settings.py
HTK_FACEBOOK_API_KEY = 'your_api_key'
HTK_FACEBOOK_API_SECRET = 'your_secret'
HTK_FACEBOOK_API_URL = 'https://api.service.com'
```

## Response Format

API responses are returned as Python dictionaries or objects:

```python
result = client.get(id='123')
print(result['name'])
print(result['created_at'])
```

## Pagination

Handle paginated responses:

```python
# Get paginated results
items = client.list(limit=100, offset=0)

# Or use iterator
for item in client.list_all():
    process(item)
```

## Caching

Cache responses when appropriate:

```python
from django.core.cache import cache

def get_resource(id):
    cache_key = f'resource_{id}'
    resource = cache.get(cache_key)

    if resource is None:
        resource = client.get(id=id)
        cache.set(cache_key, resource, 3600)

    return resource
```

## Configuration

Configure in Django settings:

```python
# settings.py
HTK_FACEBOOK_ENABLED = True
HTK_FACEBOOK_API_KEY = 'your_key'
HTK_FACEBOOK_TIMEOUT = 30
HTK_FACEBOOK_RETRIES = 3
```

## Best Practices

1. **Handle errors** - Always handle API errors gracefully
2. **Respect rate limits** - Dont exceed API rate limits
3. **Cache responses** - Cache data when appropriate
4. **Use retries** - Implement exponential backoff
5. **Validate input** - Validate data before sending to API
6. **Log operations** - Log API calls for debugging
7. **Test with sandbox** - Test in sandbox before production
