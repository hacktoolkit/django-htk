# I18N

## Classes
- **`LocalizationUsageCheck`** (i18n/dataclasses.py) - Localization Usage Check
- **`AbstractLocalizableString`** (i18n/models.py) - A localizable string is a string that can be localized to a different language.
- **`AbstractLocalizedString`** (i18n/models.py) - A localized string is one that is associated with a localizable string, and has already been translated to a local language.

## Functions
- **`add_translation`** (i18n/models.py) - Adds a translation for this `LocalizableString`
- **`is_instrumented`** (i18n/models.py) - Determines whether this localizable string is actually instrumented in the codebase.
- **`look_up_supported_languages`** (i18n/utils/data.py) - Looks up which have languages have translations.
- **`retrieve_all_strings`** (i18n/utils/data.py) - Returns all translated strings for every possible
- **`load_strings`** (i18n/utils/data.py) - Load strings from `data` into `LocalizableString` and `LocalizedString`
- **`lookup_localization`** (i18n/utils/general.py) - Looks up a `LocalizedString` key and
