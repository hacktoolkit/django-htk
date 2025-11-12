# Admin Tools Constants

> Configuration constants for HTK admin tools including pulse dashboard, user emulation, and todo management

## Purpose
This module provides configuration constants for HTK's administrative tools, including company email settings, user emulation cookies, pulse dashboard limits, and admin-specific pagination settings.

## Key Files
- `__init__.py` - Exports general admin tool constants
- `defaults.py` - Default configuration values for company settings, emulation, and todos
- `general.py` - Pulse dashboard and admin interface constants

## Key Components / Features

### Default Settings (`defaults.py`)
- `HTK_COMPANY_EMAIL_DOMAINS` - Tuple of authorized company email domains (empty by default)
- `HTK_COMPANY_OFFICER_EMAILS` - Tuple of company officer email addresses (empty by default)
- `HTK_COMPANY_EMPLOYEE_EMAILS` - Tuple of company employee email addresses (empty by default)
- `HTK_EMULATE_USER_COOKIE_EXPIRATION_MINUTES` - Cookie lifetime for user emulation (default: 15 minutes)
- `HTK_ADMINTOOLS_TODOS_CONFIGS` - List of todo configuration dataclasses (see `htk.admintools.dataclasses.TodosConfig`)

### General Admin Settings (`general.py`)
- `PULSE_RECENTLY_EDITED_PROFILES_LIMIT` - Number of recent profile edits to show (50)
- `PULSE_RECENTLY_JOINED_USERS_LIMIT` - Number of new users to display (50)
- `PULSE_RECENT_LOGINS_LIMIT` - Number of recent logins to show (50)
- `PULSE_STATS_PRECISION` - Decimal precision for statistics (4)
- `ADMINTOOLS_USER_PAGE_SIZE` - Pagination size for user listings (25)

## Usage

```python
from htk.admintools.constants import (
    HTK_EMULATE_USER_COOKIE_EXPIRATION_MINUTES,
    PULSE_RECENTLY_JOINED_USERS_LIMIT,
    ADMINTOOLS_USER_PAGE_SIZE
)

# Set user emulation cookie
response.set_cookie(
    'emulated_user_id',
    user.id,
    max_age=HTK_EMULATE_USER_COOKIE_EXPIRATION_MINUTES * 60
)

# Query recent users for pulse dashboard
recent_users = User.objects.order_by('-date_joined')[:PULSE_RECENTLY_JOINED_USERS_LIMIT]

# Paginate user list in admin
paginator = Paginator(users, ADMINTOOLS_USER_PAGE_SIZE)
```

## Related Modules
- Parent: `htk/admintools/`
- Related:
  - `htk.admintools.views` - Admin tool views using these constants
  - `htk.admintools.dataclasses` - TodosConfig dataclass definition
  - `htk.admintools.pulse` - Pulse dashboard functionality

## Notes
- Confidence: HIGH (>98%)
- Last Updated: November 2025
- Company email settings should be overridden in project settings
- User emulation feature allows admins to impersonate users for debugging
