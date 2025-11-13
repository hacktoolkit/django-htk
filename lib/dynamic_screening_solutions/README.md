# Dynamic Screening Solutions Integration

321Forms API for employee screening and onboarding.

## Quick Start

```python
from htk.lib.dynamic_screening_solutions.api import Htk321FormsAPI

api = Htk321FormsAPI()

# Get companies
companies = api.get_companies()

# Get employees by company
employees = api.get_users_by_company(company_id, user_type='employee')

# Get onboarded employees
onboarded = api.get_onboarded_employee_users_by_company(company_id)
```

## Operations

```python
# Get forms and divisions
forms = api.get_forms_by_company(company_id)
divisions = api.get_divisions_by_company(company_id)

# Get form responses
form_data = api.get_form_by_company(company_id, form_id)
user_responses = api.get_responses_by_user(user_id)

# Validate webhook
api.validate_webhook_request(request)
```

## Configuration

```python
# settings.py
DSS_API_USERNAME = os.environ.get('DSS_API_USERNAME')
DSS_API_PASSWORD = os.environ.get('DSS_API_PASSWORD')
```

## Related Modules

- `htk.apps.accounts` - User management
