# i18n App

Internationalization and localization for multi-language content.

## Overview

The `i18n` app provides:

- Localizable strings (base content in one language)
- Localized strings (translated content)
- Multi-language support
- Language detection
- Translation management

## Quick Start

### Create Translatable Strings

```python
from htk.apps.i18n.models import AbstractLocalizableString

# Create base string
base_string = AbstractLocalizableString.objects.create(
    key='greeting',
    default_value='Hello'
)

# Add translation
base_string.add_translation(language='es', value='Hola')
base_string.add_translation(language='fr', value='Bonjour')
```

### Look Up Translations

```python
from htk.apps.i18n.utils.general import lookup_localization

# Get translated string
greeting = lookup_localization('greeting', language='es')
# Returns 'Hola' or default if not found
```

### Retrieve All Strings

```python
from htk.apps.i18n.utils.data import retrieve_all_strings

# Get all translations for all languages
all_strings = retrieve_all_strings()
# {
#     'greeting': {
#         'en': 'Hello',
#         'es': 'Hola',
#         'fr': 'Bonjour'
#     }
# }
```

## Models

- **`AbstractLocalizableString`** - Base string in default language
- **`AbstractLocalizedString`** - Translation in specific language

## Common Patterns

### Language Detection

```python
from htk.apps.i18n.utils.general import detect_user_language

# Detect from request
language = detect_user_language(request)

# Set user language preference
user.profile.language = language
user.profile.save()
```

### Bulk Translation Load

```python
from htk.apps.i18n.utils.data import load_strings

data = {
    'greeting': {
        'en': 'Hello',
        'es': 'Hola',
        'fr': 'Bonjour'
    },
    'goodbye': {
        'en': 'Goodbye',
        'es': 'Adiós',
        'fr': 'Au revoir'
    }
}

load_strings(data)
```

### Check Instrumentation

```python
# Check if string is being used in code
if not base_string.is_instrumented():
    # String is defined but not used
    # Consider removing or archiving
    pass
```

## Supported Languages

```python
from htk.apps.i18n.utils.data import look_up_supported_languages

languages = look_up_supported_languages()
# ['en', 'es', 'fr', 'de', 'ja', 'zh']
```

## Configuration

```python
# settings.py
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('de', 'German'),
    ('ja', 'Japanese'),
    ('zh', 'Simplified Chinese'),
]

# Supported for i18n app
I18N_SUPPORTED_LANGUAGES = LANGUAGES
```

## Best Practices

1. **Use descriptive keys** - `app.feature.message`, not `msg_1`
2. **Keep context in values** - Provide enough info for translators
3. **Use placeholders** - For dynamic content in translations
4. **Avoid HTML in strings** - Separate content from markup
5. **Test all languages** - Verify strings render correctly
6. **Archive old strings** - Clean up unused translations
7. **Use professional translators** - Better quality than automated

## Translation Workflow

```
1. Create key in default language
2. Mark translation needed
3. Send to translators
4. Add translations via admin or load_strings()
5. Deploy and test
6. Monitor for missing translations
```

## Integration Example

```python
def render_with_language(request):
    language = request.user.profile.language or 'en'

    context = {
        'greeting': lookup_localization('greeting', language),
        'welcome': lookup_localization('welcome_message', language),
    }

    return render(request, 'page.html', context)
```
