# Constants

## Overview

This module provides comprehensive constants for global configuration, time/date calculations, geographic data, HTTP utilities, and more.

## Key Constants

### Geographic Data

```python
from htk.constants import (
    US_STATES, US_STATE_CODES_LOOKUP, US_STATES_LOOKUP,
    ALL_US_STATES_AND_TERRITORIES
)

# Get state abbreviation
state_code = US_STATE_CODES_LOOKUP['California']  # 'CA'

# Get state name from code
state_name = US_STATES_LOOKUP['NY']  # 'New York'

# List of all states (dicts with name/code pairs)
all_states = US_STATES
```

### Time Constants

```python
from htk.constants import (
    TIME_1_MINUTE_SECONDS, TIME_1_HOUR_SECONDS, TIME_1_DAY_SECONDS,
    ISOWEEKDAY_MONDAY, ISOWEEKDAY_WEEKDAYS, ISOWEEKDAY_WEEKENDS
)

# Use for delays and timeouts
timeout = 2 * TIME_1_HOUR_SECONDS  # 7200 seconds

# Check if weekday
if isoweekday in ISOWEEKDAY_WEEKDAYS:
    print("Weekday")
```

### HTTP Status Codes

```python
from htk.constants import HTTPStatus

# Access HTTP status codes
if response.status == HTTPStatus.OK:
    # response is 200
    pass
```

### Character and Text Constants

```python
from htk.constants import ALPHABET_CAPS

# Get list of capital letters
letters = ALPHABET_CAPS  # ['A', 'B', 'C', ..., 'Z']
```

### Configuration Settings

```python
from htk.constants import (
    HTK_DEFAULT_DOMAIN, HTK_SITE_NAME, HTK_DEFAULT_TIMEZONE,
    HTK_DEFAULT_COUNTRY, HTK_HANDLE_MAX_LENGTH
)

HTK_DEFAULT_DOMAIN = 'hacktoolkit.com'
HTK_SITE_NAME = 'Hacktoolkit'
HTK_DEFAULT_TIMEZONE = 'America/Los_Angeles'
HTK_DEFAULT_COUNTRY = 'US'
HTK_HANDLE_MAX_LENGTH = 64
```

## Subdirectories

- **dns/**: DNS and TLD constants
- **emails/**: Email validation patterns and common handles
- **i18n/**: International constants (countries, currencies, languages, timezones)

## Customization

Override defaults in `settings.py`:

```python
HTK_SITE_NAME = 'My Site'
HTK_DEFAULT_TIMEZONE = 'UTC'
HTK_DEFAULT_DOMAIN = 'example.com'
```
