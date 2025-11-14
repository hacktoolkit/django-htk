# Cache Constants

## Overview

This module defines configuration constants for Django cache settings.

## Configuration Settings

```python
from htk.cache.constants import HTK_CACHE_KEY_PREFIX

# Prefix prepended to all cache keys (default: 'htk')
HTK_CACHE_KEY_PREFIX = 'htk'
```

## Customization

Override this setting in `settings.py`:

```python
# Use a custom cache key prefix
HTK_CACHE_KEY_PREFIX = 'myapp'
```

## Usage

Cache utilities throughout the codebase use this prefix to namespace cache keys:

```python
# Cache key will be prefixed: 'htk:user:123:data'
cache_key = f"{HTK_CACHE_KEY_PREFIX}:user:123:data"
```
