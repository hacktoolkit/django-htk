# HTK Utils Module

> 24 categories of utility functions for text, data, HTTP, encryption, and more.

## Purpose

The utils module provides reusable utility functions for common tasks: text processing, data structures, date/time handling, database operations, HTTP requests, encryption, and specialized domains like i18n, math, and measurements.

## Subdirectories

| Module | Purpose |
|--------|---------|
| **[text/](text/README.md)** | Text transformation, sanitization, algorithms, Unicode handling |
| **[data_structures/](data_structures/README.md)** | Chunking, sliding windows, lookahead iterators |
| **[http/](http/README.md)** | HTTP request/response helpers, error handling |
| **[i18n/](i18n/README.md)** | Language, country, and localization utilities |
| **[log/](log/README.md)** | Logging handlers for Rollbar, Slack, and backends |
| **[maths/](maths/README.md)** | Clamping, normalization, percentages |
| **[measurements/](measurements/README.md)** | Distance, weight, temperature conversion |
| **[concurrency/](concurrency/README.md)** | Threading and parallel execution |

## Quick Start

```python
from htk.utils.datetime_utils import utcnow
from htk.utils.db import get_object_or_none
from htk.utils.text.transformers import to_snake_case

# UTC time
now = utcnow()

# Safe lookup
user = get_object_or_none(User, email='user@example.com')

# Text transformation
slug = to_snake_case('User Name')
```

## Common Utilities

| Utility | Purpose |
|---------|---------|
| **datetime_utils** | `utcnow()`, timestamps, timezone handling |
| **db** | `get_object_or_none()`, `bulk_update()`, raw queries |
| **text** | Case conversion, sanitization, algorithms |
| **data_structures** | `chunks()`, `lookahead()`, `sliding_window()` |
| **crypto** | `hash_string()`, `encrypt_string()`, `decrypt_string()` |
| **request** | `get_client_ip()`, `is_https()`, `is_ajax()` |
| **email** | `send_email()`, `send_templated_email()` |
| **handles** | `generate_handle()`, `slugify()`, uniqueness |
| **json_utils** | `to_json_serializable()`, safe encoding/decoding |
| **cache_descriptors** | `CachedProperty`, `CachedAttribute` with timeout |

## Usage Patterns

### Safe Object Lookup

```python
from htk.utils.db import get_object_or_none

user = get_object_or_none(User, email=email)
if user:
    # Process existing user
else:
    # Create new user
```

### Batch Processing

```python
from htk.utils.data_structures import chunks

for batch in chunks(items, batch_size=100):
    process_batch(batch)
    db.commit()
```

### Caching Expensive Operations

```python
from htk.utils.cache_descriptors import CachedProperty

class Account(models.Model):
    @CachedProperty(timeout=86400)
    def total_balance(self):
        return self.transactions.aggregate(Sum('amount'))
```

### Text Processing

```python
from htk.utils.text.transformers import to_snake_case
from htk.utils.text.sanitizers import sanitize_html

clean = sanitize_html(user_input)
normalized = to_snake_case(clean)
```

### Email with Template

```python
from htk.utils.email import send_templated_email

send_templated_email(
    to=['user@example.com'],
    template='password_reset',
    context={'user': request.user, 'url': reset_url}
)
```

## Key Modules

**crypto.py** - Password hashing and encryption
```python
from htk.utils.crypto import hash_string, verify_hash

hashed = hash_string(password)
if verify_hash(password, hashed):
    # Correct password
```

**base_converters.py** - Base36/Base62 encoding (short URLs)
```python
from htk.utils.base_converters import base36_encode

short_code = base36_encode(123456789)  # 'kf12oi'
```

**currency.py** - Currency conversion
```python
from htk.utils.currency import convert_currency, format_currency

usd = convert_currency(100, 'EUR', 'USD')
display = format_currency(1000, 'USD')  # "$1,000.00"
```

**enums.py** - Enum to Django choices conversion
```python
from htk.utils.enums import enum_to_choices

CHOICES = enum_to_choices(StatusEnum)
```

## Best Practices

- **Check utils first** before writing custom code to avoid duplication
- **Cache expensive operations** using `CachedProperty` or HTK cache module
- **Use `get_object_or_none()`** instead of try/except for cleaner code
- **Batch operations** with `chunks()` for large datasets to avoid memory issues

## Testing

```python
from django.test import TestCase
from htk.utils.datetime_utils import utcnow
from django.utils import timezone

class UtilsTestCase(TestCase):
    def test_utcnow(self):
        """Verify utcnow returns UTC timezone-aware datetime."""
        result = utcnow()
        self.assertEqual(result.tzinfo, timezone.utc)
```

## Related Modules

- `htk.cache` - Caching framework with descriptors
- `htk.validators` - Data validation helpers
- `htk.decorators` - Reusable function decorators
- `htk.extensions` - Extended data structures

## References

- [Python Standard Library](https://docs.python.org/3/library/)
- [Django Utilities](https://docs.djangoproject.com/en/stable/ref/utils/)

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
