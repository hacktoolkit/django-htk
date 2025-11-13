# Utils

## Overview

This utils module provides utility functions for common operations including lookups, transformations, validation, and calculations.

## Quick Start

### Import Utilities

```python
from htk.apps.accounts.utils.utils import function_name

result = function_name(arg1, arg2)
```

### Common Patterns

```python
# Lookup by identifier
item = get_item_by_id(id)

# Get or None
item = get_item_by_email(email)  # Returns None if not found

# Create with defaults
item = create_item(name='test')

# Query collection
items = get_active_items()

# Transform/convert
converted = convert_format(data)
```

## Utility Functions

### Lookup Functions

Functions that retrieve objects from the database:

- `get_*_by_id()` - Get by primary key
- `get_*_by_field()` - Get by specific field
- `get_*_with_retries()` - With retry logic
- `get_all_*()` - Get all objects
- `get_inactive_*()` - Get filtered subset

**Behavior:**
- Return `None` if object not found (not exception)
- Raise exception on database errors
- Support optional filtering parameters

### Creation Functions

Functions that create new objects:

- `create_*()` - Create new object
- `set_*()` - Update single field

**Behavior:**
- Return created object
- May have side effects (logging, signals)
- Validate input before creation

### Validation Functions

Functions that validate data:

- `validate_*()` - Validate and return boolean
- `is_*()` - Check condition

**Behavior:**
- Return `True`/`False` for simple checks
- Return object or tuple for complex validation
- May raise exception on invalid data

### Transformation Functions

Functions that convert or transform data:

- `convert_*()` - Convert between formats
- `extract_*()` - Extract data from object
- `generate_*()` - Generate new data

## Function Conventions

- **Return values:** `None` when object not found, exception on error
- **Naming:** `get_*()` for retrieval, `create_*()` for creation
- **Parameters:** Use keyword arguments for optional parameters
- **Side effects:** Document any side effects in docstring
- **Retry logic:** Use `*_with_retries()` variant for reliability

## Configuration

Configure behavior in Django settings:

```python
# settings.py
HTK_SETTING_NAME = 'value'
HTK_TIMEOUT = 30
HTK_MAX_RETRIES = 3
```

## Best Practices

1. **Check for None** - Always check return values for None
2. **Handle exceptions** - Catch and handle domain exceptions
3. **Use appropriate function** - Choose most specific function available
4. **Understand side effects** - Read docstrings for side effects
5. **Batch operations** - Use bulk_* variants when processing multiple items
6. **Cache results** - Cache expensive lookups when appropriate
7. **Test edge cases** - Test with missing data, invalid input, etc.
