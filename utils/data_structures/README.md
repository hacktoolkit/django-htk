# Data Structures Utils

## Overview

This module provides utility functions for working with dictionaries and other data structures.

## Functions

### Dictionary Filtering

```python
from htk.utils.data_structures import filter_dict

def filter_dict(d, keys):
    """Filter a dictionary to only include specified keys.

    Args:
        d: Dictionary to filter
        keys: Iterable of keys to keep

    Returns:
        New dictionary with only the specified keys
    """

# Filter a dictionary
original = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
filtered = filter_dict(original, ['a', 'c'])
# Result: {'a': 1, 'c': 3}
```

## Usage Examples

### Keep Only Specific Fields

```python
from htk.utils.data_structures import filter_dict

user_data = {
    'id': 123,
    'name': 'John',
    'email': 'john@example.com',
    'password_hash': 'secret...',
    'api_key': 'key...'
}

# Extract only safe fields for API response
safe_fields = filter_dict(user_data, ['id', 'name', 'email'])
# {'id': 123, 'name': 'John', 'email': 'john@example.com'}
```

### Build Dynamic Queries

```python
from htk.utils.data_structures import filter_dict

params = {
    'search': 'query',
    'sort': 'name',
    'limit': 10,
    'internal_flag': False,
    'debug': True
}

# Keep only API-safe parameters
api_params = filter_dict(params, ['search', 'sort', 'limit'])
```
