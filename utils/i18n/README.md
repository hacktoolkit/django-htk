# Internationalization Utilities

Language, locale, and country utilities.

## Quick Start

```python
from htk.utils.i18n.general import get_country_choices

# Get list of country choices for form
country_choices = get_country_choices()
# Returns: [('US', 'United States'), ('GB', 'United Kingdom'), ...]
```

## Common Patterns

```python
# Use in Django form
class AddressForm(forms.Form):
    country = forms.ChoiceField(choices=get_country_choices())
```

## Related Modules

- `htk.apps.i18n` - Internationalization app
- `htk.constants` - ISO country codes
