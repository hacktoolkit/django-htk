# Constants

Project-wide constants and enumerations.

## Overview

The `constants` module provides:

- HTTP status codes
- DNS record types
- Email constants
- Internationalization constants
- Common values used across the app

## HTTP Status Codes

Convenient access to HTTP status codes:

```python
from htk.constants.http import HTTPStatus

# Use as strings or integers
if response.status_code == HTTPStatus.OK:
    print('Success!')

assert HTTPStatus.NOT_FOUND == 404
assert HTTPStatus.UNAUTHORIZED == 401
```

**Common Codes:**
- `OK` (200)
- `CREATED` (201)
- `BAD_REQUEST` (400)
- `UNAUTHORIZED` (401)
- `FORBIDDEN` (403)
- `NOT_FOUND` (404)
- `CONFLICT` (409)
- `INTERNAL_SERVER_ERROR` (500)

## DNS Constants

DNS record types for DNS lookups:

```python
from htk.constants.dns import DNSRecordType

record_type = DNSRecordType.MX  # Mail exchange
record_type = DNSRecordType.A   # Address (IPv4)
record_type = DNSRecordType.TXT # Text records
```

## Email Constants

Email-related constants:

```python
from htk.constants.emails import EmailStatus, EmailType

status = EmailStatus.SENT
email_type = EmailType.NOTIFICATION
```

## Internationalization

Language and locale constants:

```python
from htk.constants.i18n import COMMON_LANGUAGES, SUPPORTED_LANGUAGES

language = COMMON_LANGUAGES.ENGLISH
language_code = 'en-US'
```

## Usage Patterns

### Status Code Responses

```python
from django.http import JsonResponse
from htk.constants.http import HTTPStatus

def api_endpoint(request):
    if not request.user:
        return JsonResponse(
            {'error': 'Not authenticated'},
            status=HTTPStatus.UNAUTHORIZED
        )
    return JsonResponse({'data': []}, status=HTTPStatus.OK)
```

### Conditional Logic

```python
from htk.constants.http import HTTPStatus

response = requests.get('https://api.example.com/data')

if response.status_code == HTTPStatus.OK:
    data = response.json()
elif response.status_code == HTTPStatus.NOT_FOUND:
    log.warning('Resource not found')
elif response.status_code >= 500:
    log.error(f'Server error: {response.status_code}')
```

## Organizing Your Own Constants

Follow this pattern for application-specific constants:

```python
# myapp/constants.py
from enum import Enum

class UserRole(Enum):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

class PaymentStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'

# Usage
if user.role == UserRole.ADMIN:
    can_delete = True
```

## Best Practices

1. **Use constants instead of magic strings** - `HTTPStatus.OK` not `200`
2. **Group related constants** - Organize by feature or domain
3. **Use enums for sets** - `PaymentStatus` with fixed options
4. **Document meanings** - Add docstrings to clarify intent
5. **Version with migrations** - Be careful changing constants in production

## File Organization

```
constants/
├── __init__.py
├── http.py          # HTTP status codes
├── dns.py           # DNS record types
├── emails.py        # Email constants
├── i18n.py          # Internationalization
└── README.md
```

## Related Modules

- `django.http` - Django HTTP status codes
- `htk.utils` - Utility functions
- `htk.validators` - Validation functions
