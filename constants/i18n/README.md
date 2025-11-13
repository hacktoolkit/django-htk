# Internationalization Constants

## Overview

This module provides constants for international applications including country data, currencies, languages, greetings, and timezones.

## Constants

### Countries

```python
from htk.constants.i18n import COUNTRIES_EN_NAMES_MAP

# Dictionary mapping country codes to English names
# e.g. {'US': 'United States', 'CA': 'Canada', 'GB': 'United Kingdom', ...}
countries = COUNTRIES_EN_NAMES_MAP
```

### Currencies

```python
from htk.constants.i18n import CURRENCY_CODE_TO_SYMBOLS_MAP

# Dictionary mapping currency codes to symbols
symbols = CURRENCY_CODE_TO_SYMBOLS_MAP
# {'USD': '$', 'EUR': '€', 'GBP': '£', ...}
```

### Languages

```python
from htk.constants.i18n import LANGUAGE_EN_NAMES_MAP, LANGUAGE_NAMES_MAP

# Language codes to English names
english_names = LANGUAGE_EN_NAMES_MAP
# {'de': 'German', 'en': 'English', 'es': 'Spanish', ...}

# Language codes to native language names
native_names = LANGUAGE_NAMES_MAP
# {'de': 'Deutsch', 'en': 'English', 'es': 'Español', ...}
```

### Greetings

```python
from htk.constants.i18n import I18N_GREETINGS

# Greetings in multiple languages
# {'am': 'ሰላም', 'ar': 'مرحبا', 'en': 'Hello', 'es': 'Hola', ...}
greetings = I18N_GREETINGS
```

### Timezones

```python
from htk.constants.i18n import US_TIMEZONE_CHOICES

# Tuple of (IANA timezone, legacy US timezone) tuples
# Used for Django form choice fields
timezone_choices = US_TIMEZONE_CHOICES
# (('America/New_York', 'Eastern Time (US & Canada)'), ...)
```

### English Language Helpers

```python
from htk.constants.i18n import SPECIAL_NOUN_PLURAL_FORMS

# Dictionary mapping nouns to their plural forms (irregular plurals)
plurals = SPECIAL_NOUN_PLURAL_FORMS
# {'child': 'children', 'person': 'people', ...}
```

## Usage Examples

### Get Country Name

```python
from htk.constants.i18n import COUNTRIES_EN_NAMES_MAP

country_code = 'US'
country_name = COUNTRIES_EN_NAMES_MAP.get(country_code)
# 'United States'
```

### Format Currency

```python
from htk.constants.i18n import CURRENCY_CODE_TO_SYMBOLS_MAP

def format_price(amount, currency_code):
    """Format price with currency symbol."""
    symbol = CURRENCY_CODE_TO_SYMBOLS_MAP.get(currency_code, '')
    return f"{symbol}{amount:.2f}"

formatted = format_price(99.99, 'USD')
# '$99.99'
```

### Get Plural Form

```python
from htk.constants.i18n import SPECIAL_NOUN_PLURAL_FORMS

def pluralize(noun):
    """Get plural form of noun."""
    return SPECIAL_NOUN_PLURAL_FORMS.get(noun, f"{noun}s")

plural = pluralize('child')
# 'children'
```
