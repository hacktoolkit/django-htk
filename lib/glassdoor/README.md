# Glassdoor Integration

Company information and reviews.

## Quick Start

```python
from htk.lib.glassdoor.utils import get_company_info

# Get company details
company = get_company_info(company_id)
print(company['name'], company['rating'], company['reviews'])
```

## Configuration

```python
# settings.py
GLASSDOOR_API_KEY = os.environ.get('GLASSDOOR_API_KEY')
```

## Related Modules

- `htk.lib.linkedin` - Professional networking
- `htk.apps.customers` - Employer/company profiles
