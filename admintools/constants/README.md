# Admin Tools Constants

## Overview

This module provides configuration constants for the admin tools dashboard and user emulation features.

## Configuration Settings

```python
from htk.admintools.constants import (
    HTK_COMPANY_EMAIL_DOMAINS,
    HTK_COMPANY_OFFICER_EMAILS,
    HTK_COMPANY_EMPLOYEE_EMAILS,
    HTK_EMULATE_USER_COOKIE_EXPIRATION_MINUTES,
    HTK_ADMINTOOLS_TODOS_CONFIGS
)

# Email domains that identify company employees
HTK_COMPANY_EMAIL_DOMAINS = ()  # e.g. ('company.com', 'internal.company.com')

# Email addresses of company officers
HTK_COMPANY_OFFICER_EMAILS = ()  # e.g. ('ceo@company.com', 'cto@company.com')

# Email addresses of all company employees
HTK_COMPANY_EMPLOYEE_EMAILS = ()  # Subset of HTK_COMPANY_OFFICER_EMAILS

# Session timeout for user emulation (minutes)
HTK_EMULATE_USER_COOKIE_EXPIRATION_MINUTES = 15

# List of admin todo configurations
HTK_ADMINTOOLS_TODOS_CONFIGS = []
```

## Dashboard Constants

```python
from htk.admintools.constants import (
    PULSE_RECENTLY_EDITED_PROFILES_LIMIT,
    PULSE_RECENTLY_JOINED_USERS_LIMIT,
    PULSE_RECENT_LOGINS_LIMIT,
    PULSE_STATS_PRECISION,
    ADMINTOOLS_USER_PAGE_SIZE
)

# Dashboard data limits
PULSE_RECENTLY_EDITED_PROFILES_LIMIT = 50
PULSE_RECENTLY_JOINED_USERS_LIMIT = 50
PULSE_RECENT_LOGINS_LIMIT = 50

# Decimal precision for statistics
PULSE_STATS_PRECISION = 4

# User list pagination
ADMINTOOLS_USER_PAGE_SIZE = 25
```

## Customization

Override these settings in `settings.py`:

```python
HTK_COMPANY_EMAIL_DOMAINS = ('acme.com', 'acme.internal')
HTK_EMULATE_USER_COOKIE_EXPIRATION_MINUTES = 30
PULSE_RECENTLY_EDITED_PROFILES_LIMIT = 100
```
