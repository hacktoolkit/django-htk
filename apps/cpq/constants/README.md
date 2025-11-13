# Constants

Configuration and constant values for this module.

## Overview

This constants module defines configuration values, enumerations, lookup tables, and other constant data used throughout the module. Constants are organized into sub-modules by category.

## Module Structure

```
constants/
├── __init__.py          # Re-exports all constants
├── general.py           # General purpose constants
├── defaults.py          # Configuration defaults (HTK_ prefixed settings)
└── domain_specific.py          # Domain-specific constants
```

## Types of Constants

### Configuration Settings (HTK_ Prefix)

Settings that can be overridden in Django settings:

```python
from htk.apps.cpq.constants import HTK_SETTING_NAME

# Configure in settings.py
HTK_SETTING_NAME = 'custom_value'
```

### Enumerations

Enum classes for status values, roles, and choices:

```python
from htk.apps.cpq.constants import SomeEnum

status = SomeEnum.ACTIVE
value = status.value
name = status.name
```

### Lookup Tables

Dictionaries and data collections for reference:

```python
from htk.apps.cpq.constants import LOOKUP_TABLE

data = LOOKUP_TABLE['key']
for key, value in LOOKUP_TABLE.items():
    # Process each entry
```

### Conversion Factors

Numeric constants for unit conversions and calculations:

```python
from htk.constants import TIME_1_HOUR_SECONDS

delay = 2 * TIME_1_HOUR_SECONDS  # 2 hours in seconds
```

## Usage Examples

### Import Constants

```python
# Import from constants module
from htk.apps.cpq.constants import CONSTANT_NAME

# Or import directly from sub-module
from htk.apps.cpq.constants.general import CONSTANT_NAME
```

### Access Enum Values

```python
from htk.apps.cpq.constants import StatusEnum

if status == StatusEnum.ACTIVE:
    print(f"Status is {status.name}")
```

### Use Lookup Tables

```python
from htk.apps.cpq.constants import LOOKUP_DATA

# Get value by key
value = LOOKUP_DATA.get('key')

# Iterate over entries
for key, value in LOOKUP_DATA.items():
    process(key, value)
```

## Configuration

Settings can be overridden in Django settings.py:

```python
# settings.py
HTK_SETTING_NAME = 'custom_value'
HTK_TIMEOUT_SECONDS = 300
HTK_ENABLED = True
```
