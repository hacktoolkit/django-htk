# Internationalization (i18n) Constants

## Overview

This module provides configuration for localization and internationalization, including model references and language settings.

## Constants

### Model References

- **`HTK_LOCALIZABLE_STRING_MODEL`** - Default: `None` - Localizable string model (app_label.ModelName)
- **`HTK_LOCALIZED_STRING_MODEL`** - Default: `None` - Localized string model (app_label.ModelName)

### Language Configuration

- **`HTK_LOCALIZABLE_STRING_LANGUAGE_CODES`** - Default: `['en-US']` - List of supported language codes

### Admin Tools

- **`HTK_ADMINTOOLS_LOCALIZATION_USAGE_CHECKS`** - Default: `[]` - List of localization usage checks

## Usage Examples

### Configure Language Support

```python
# In Django settings.py
HTK_LOCALIZABLE_STRING_LANGUAGE_CODES = [
    'en-US',
    'es-ES',
    'fr-FR',
    'de-DE',
]
```

### Set Custom Models

```python
# In Django settings.py
HTK_LOCALIZABLE_STRING_MODEL = 'myapp.LocalizableString'
HTK_LOCALIZED_STRING_MODEL = 'myapp.LocalizedString'
```

### Load Model References

```python
from django.apps import apps
from htk.apps.i18n.constants import (
    HTK_LOCALIZABLE_STRING_MODEL,
    HTK_LOCALIZED_STRING_MODEL,
)

LocalizableString = apps.get_model(HTK_LOCALIZABLE_STRING_MODEL)
LocalizedString = apps.get_model(HTK_LOCALIZED_STRING_MODEL)
```
