# HTK Constants Module

> Application-wide constants for geographic, temporal, i18n, email, and DNS data.

## Purpose

The constants module centralizes all application-wide constants used throughout HTK and projects. It provides a single source of truth for magic numbers, strings, and configuration values, making code more maintainable and less prone to typos.

## Quick Start

```python
from htk.constants.time import TIMEOUT_1_HOUR, TIMEOUT_1_DAY
from htk.constants.geo import US_STATE_CHOICES, COUNTRY_CHOICES
from htk.constants.alphabet import ALPHANUMERIC_UPPER
from django.core.cache import cache

# Cache for 1 hour
cache.set('key', 'value', TIMEOUT_1_HOUR)

# Use in model field choices
state_field = models.CharField(choices=US_STATE_CHOICES, max_length=2)

# Generate random code
import random
code = ''.join(random.choice(ALPHANUMERIC_UPPER) for _ in range(8))
```

## Key Constants

| Category | Module | Use Case |
|----------|--------|----------|
| **Time** | `time.py` | Cache timeouts, task delays, expiration (TIMEOUT_1_HOUR, etc.) |
| **Geography** | `geo.py` | US states, countries, region data (US_STATE_CHOICES, COUNTRY_CHOICES) |
| **HTTP** | `http.py` | HTTP status codes (HTTP_STATUS_OK, HTTP_STATUS_NOT_FOUND) |
| **Alphabet** | `alphabet.py` | Character sets for validation/generation (ALPHANUMERIC, VOWELS) |
| **i18n** | `i18n/` | Languages, countries, currencies, timezones, greetings |
| **Email** | `emails/` | Email subject templates, patterns, business handles |
| **DNS** | `dns/` | DNS record types, MX priority levels |
| **Defaults** | `defaults.py` | Default configuration values |

## Common Patterns

### Time Constants for Caching and Tasks

```python
from htk.constants.time import (
    TIMEOUT_1_MINUTE,    # 60 seconds
    TIMEOUT_5_MINUTES,   # 300 seconds
    TIMEOUT_30_MINUTES,  # 1800 seconds (default)
    TIMEOUT_1_HOUR,      # 3600 seconds
    TIMEOUT_1_DAY,       # 86400 seconds
    TIMEOUT_1_WEEK,      # 604800 seconds
    TIMEOUT_NONE,        # None (cache forever)
)

# Use with cache
from django.core.cache import cache
cache.set('user_prefs', data, TIMEOUT_1_HOUR)

# Use with models
class Product(models.Model, CacheableObject):
    def get_cache_duration(self):
        return TIMEOUT_1_DAY  # Cache product for 1 day
```

### Geographic and i18n Constants

```python
from htk.constants.geo import US_STATE_CHOICES, COUNTRY_CHOICES
from htk.constants.i18n.languages import LANGUAGE_CHOICES
from htk.constants.i18n.currencies import CURRENCY_CHOICES

class Address(models.Model):
    state = models.CharField(max_length=2, choices=US_STATE_CHOICES)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)

class UserProfile(models.Model):
    preferred_language = models.CharField(
        max_length=5, choices=LANGUAGE_CHOICES, default='en'
    )
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, default='USD'
    )
```

### Character Sets for Code Generation

```python
from htk.constants.alphabet import ALPHANUMERIC_UPPER, VOWELS, CONSONANTS
import random

def generate_coupon_code(length=8):
    """Generate random alphanumeric coupon code"""
    return ''.join(random.choice(ALPHANUMERIC_UPPER) for _ in range(length))

def generate_pronounceable_password(length=12):
    """Generate easier-to-read password (consonant-vowel pattern)"""
    password = ''
    for i in range(length):
        if i % 2 == 0:
            password += random.choice(CONSONANTS)
        else:
            password += random.choice(VOWELS)
    return password.upper()
```

## Organization

All constants are organized by domain:

- **Primary files** - `time.py`, `geo.py`, `http.py`, `alphabet.py`, `defaults.py`, `units.py`
- **Subdirectories** - `i18n/` (languages, countries, currencies), `emails/`, `dns/`

Naming conventions:
- `TIMEOUT_*` - Cache/task timeout durations
- `*_CHOICES` - Django model field choices
- `*_STATUS` - Status or state values
- `*_CODES` - Code mappings

## Best Practices

- **Use constants instead of magic values** - `TIMEOUT_1_HOUR` instead of `3600`
- **Group related constants together** - Keep related values in the same file
- **Document non-obvious values** - Add comments with units (seconds, pixels)
- **Import strategically** - Import only what you need, avoid star imports
- **Update in one place** - Define once, reference everywhere

## Testing

```python
from django.test import TestCase
from htk.constants.time import TIMEOUT_1_HOUR
from htk.constants.geo import US_STATE_CHOICES

class ConstantsTestCase(TestCase):
    def test_timeout_values(self):
        """Verify timeout constants are correct integers"""
        self.assertIsInstance(TIMEOUT_1_HOUR, int)
        self.assertEqual(TIMEOUT_1_HOUR, 3600)

    def test_choice_tuples(self):
        """Verify choice constants have proper tuple format"""
        self.assertTrue(len(US_STATE_CHOICES) > 0)
        # Each choice should be a (value, label) tuple
        for value, label in US_STATE_CHOICES:
            self.assertIsInstance(value, str)
            self.assertIsInstance(label, str)
```

## Related Modules

- `htk.cache` - Uses time constants
- `htk.constants.time` - Cache/task timeouts
- `htk.constants.geo` - Geographic data
- `htk.constants.i18n` - Language/localization
- `htk.constants.emails` - Email configuration
- `htk.constants.dns` - DNS records

## References

- [Django Model Field Choices](https://docs.djangoproject.com/en/stable/ref/models/fields/#choices)
- [Python Enum Documentation](https://docs.python.org/3/library/enum.html)
- ISO Standards for Countries, Languages, and Currencies

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
