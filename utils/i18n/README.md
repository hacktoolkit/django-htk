# Internationalization Utils

## Overview

This module provides utility functions for working with international data including countries, languages, currencies, and timezones.

## Functions

```python
from htk.utils.i18n import (
    get_country_choices,
    get_language_name,
    get_currency_symbol,
    get_random_greeting
)

# Get country choices for form select fields
choices = get_country_choices(ordering=('US', 'CA'))

# Get language name from code
lang_name = get_language_name('en')  # 'English'

# Get currency symbol
symbol = get_currency_symbol('USD')  # '$'

# Get random greeting in random language
greeting = get_random_greeting()  # e.g. 'Hola'
```

## Usage Examples

### Form Select Choices

```python
from htk.utils.i18n import get_country_choices

class LocationForm(forms.Form):
    country = forms.ChoiceField(
        choices=get_country_choices(ordering=('US', 'CA', 'MX')),
        help_text="Select your country"
    )
```

### Display Language Names

```python
from htk.utils.i18n import get_language_name

supported_languages = ['en', 'es', 'fr', 'de']
for lang_code in supported_languages:
    print(f"{lang_code}: {get_language_name(lang_code)}")
    # en: English
    # es: Spanish
    # fr: French
    # de: German
```

### Format Prices with Currency Symbols

```python
from htk.utils.i18n import get_currency_symbol

def format_price(amount, currency_code):
    symbol = get_currency_symbol(currency_code)
    return f"{symbol}{amount:.2f}"

print(format_price(99.99, 'USD'))   # $99.99
print(format_price(99.99, 'EUR'))   # €99.99
```

### Randomized Greetings

```python
from htk.utils.i18n import get_random_greeting

# Use for welcome banners or dashboard headers
greeting = get_random_greeting()
```
