# HTK i18n Utils

Utilities for internationalization including language data management, string retrieval, and localization lookups.

## Functions by Category

### Data Functions

**look_up_supported_languages()**
- Gets all language codes with translations (cached with lru_cache)
- Returns list of language codes ordered alphabetically
- Example: ['en-US', 'es-ES', 'zh-CN']

**retrieve_all_strings(by_language=False, language_codes=None, namespaces=None)**
- Retrieves all translated strings with flexible organization
- When by_language=False: Returns dict keyed by string key with language translations
- When by_language=True: Returns dict keyed by language code with string translations
- Optional language_codes and namespaces filtering
- Returns nested dict structure with full translation data

**dump_strings(file_path, indent=4, by_language=False, language_codes=None)**
- Exports all strings to JSON file
- Creates directory structure if needed
- Returns count of strings dumped

**load_strings(data, overwrite=False)**
- Imports strings from dict into LocalizableString and LocalizedString
- When overwrite=False: Only adds new translations
- When overwrite=True: Updates existing translations
- Returns tuple: (num_strings, num_translations)

### Utility Functions

**get_language_code_choices()**
- Gets language code choices for forms
- Returns list of (code, code) tuples from HTK_LOCALIZABLE_STRING_LANGUAGE_CODES
- Example: [('en-US', 'en-US'), ('es-ES', 'es-ES')]

**lookup_localization(key=None, locale='en-US')**
- Looks up a localized string by key and language
- Returns localized value or fallback error string if not found
- Fallback format: '???[key]-[locale]???'

## Data Structure Examples

### retrieve_all_strings(by_language=False)
```json
{
  "welcome_title": {
    "en-US": "Welcome",
    "es-ES": "Bienvenido"
  },
  "goodbye_title": {
    "en-US": "Goodbye",
    "es-ES": "Adiós"
  }
}
```

### retrieve_all_strings(by_language=True)
```json
{
  "en-US": {
    "welcome_title": "Welcome",
    "goodbye_title": "Goodbye"
  },
  "es-ES": {
    "welcome_title": "Bienvenido",
    "goodbye_title": "Adiós"
  }
}
```

## Example Usage

```python
from htk.apps.i18n.utils import (
    look_up_supported_languages,
    lookup_localization,
    retrieve_all_strings,
    dump_strings,
)

# Get supported languages
langs = look_up_supported_languages()

# Lookup a string
welcome = lookup_localization('welcome_title', locale='es-ES')

# Export strings
dump_strings('/tmp/translations.json')

# Import strings
data = retrieve_all_strings(by_language=False)
count = load_strings(data)
```
