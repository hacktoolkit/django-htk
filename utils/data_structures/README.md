# Data Structures Utilities

Dictionary and collection utilities.

## Quick Start

```python
from htk.utils.data_structures.general import filter_dict

# Filter dictionary to specific keys
data = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
filtered = filter_dict(data, ['a', 'c'])  # {'a': 1, 'c': 3}
```

## Common Patterns

```python
# Extract subset of data
user_data = {'id': 1, 'name': 'John', 'email': 'john@example.com', 'password_hash': 'xxx'}
safe_data = filter_dict(user_data, ['id', 'name', 'email'])
```

## Related Modules

- `htk.extensions` - OrderedSet and data structures
