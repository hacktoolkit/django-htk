# Dynamic Screening Solutions (321forms) Constants

Configuration constants and API endpoints for 321forms HR screening integration.

## Configuration Settings

```python
from htk.lib.dynamic_screening_solutions.constants import (
    HTK_321FORMS_USERNAME,
    HTK_321FORMS_SECRET,
    HTK_321FORMS_ENTRY_POINT_URL,
    HTK_321FORMS_WEBHOOK_HASH_KEY_RETRIEVER,
    HTK_321FORMS_WEBHOOK_EVENT_HANDLERS,
)
```

## API Configuration

```python
# settings.py
HTK_321FORMS_USERNAME = 'your-username'
HTK_321FORMS_SECRET = 'your-api-secret'
HTK_321FORMS_ENTRY_POINT_URL = 'https://api.321forms.com/v1/'
```

## Webhook Configuration

```python
# Webhook event handlers
HTK_321FORMS_WEBHOOK_EVENT_HANDLERS = {
    'all_forms_submitted': 'your.module.handlers.all_forms_submitted',
    'custom_event': 'your.module.handlers.custom_event',
    'form_approved': 'your.module.handlers.form_approved',
    'form_submitted': 'your.module.handlers.form_submitted',
    'onboarding_complete': 'your.module.handlers.onboarding_complete',
    'status_change': 'your.module.handlers.status_change',
}
```

## API Resources

```python
from htk.lib.dynamic_screening_solutions.constants import (
    DSS_321FORMS_API_RESOURCE_USER,
    DSS_321FORMS_API_RESOURCE_USER_FORMS,
    DSS_321FORMS_API_RESOURCE_COMPANY_USERS,
)

# User resources
user_url = DSS_321FORMS_API_RESOURCE_USER % {'user_id': '123'}
user_forms_url = DSS_321FORMS_API_RESOURCE_USER_FORMS % {'user_id': '123'}

# Company resources
company_users_url = DSS_321FORMS_API_RESOURCE_COMPANY_USERS % {
    'company_id': '456',
    'user_type': 'employee',
}
```

## User Types

```python
from htk.lib.dynamic_screening_solutions.constants import (
    DSS_321FORMS_API_USER_TYPE_HR_STAFF,
    DSS_321FORMS_API_USER_TYPE_HR_ADMIN,
    DSS_321FORMS_API_USER_TYPE_EMPLOYEE,
    DSS_321FORMS_API_USER_TYPE_EMPLOYEE_COMPLETE,
)
```
