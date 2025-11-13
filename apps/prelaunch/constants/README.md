# Prelaunch Constants

## Overview

This module provides configuration for prelaunch/beta mode, including feature toggles, URL settings, email templates, and exception lists for views that bypass prelaunch restrictions.

## Constants

### Feature Toggle

- **`HTK_PRELAUNCH_MODE`** - Default: `False` - Enable prelaunch mode to restrict access

### Model and Form Configuration

- **`HTK_PRELAUNCH_MODEL`** - Default: `'htk.PrelaunchSignup'` - Prelaunch signup model
- **`HTK_PRELAUNCH_FORM_CLASS`** - Default: `'htk.apps.prelaunch.forms.PrelaunchSignupForm'` - Signup form class

### URL Configuration

- **`HTK_PRELAUNCH_URL_NAME`** - Default: `'htk_prelaunch'` - URL name for prelaunch page
- **`HTK_PRELAUNCH_HOST_REGEXPS`** - Default: `[]` - Regex patterns for hosts to apply prelaunch

### Exception Lists

- **`HTK_PRELAUNCH_EXCEPTION_VIEWS`** - Views exempt from prelaunch redirect (URL names)
- **`HTK_PRELAUNCH_EXCEPTION_URLS`** - URL patterns exempt from prelaunch redirect (regex)

### Template Configuration

- **`HTK_PRELAUNCH_TEMPLATE`** - Default: `'htk/prelaunch.html'` - Prelaunch signup page template
- **`HTK_PRELAUNCH_SUCCESS_TEMPLATE`** - Default: `None` - Template shown after signup

### Email Configuration

- **`HTK_PRELAUNCH_EMAIL_TEMPLATE`** - Default: `'htk/prelaunch'` - Confirmation email template
- **`HTK_PRELAUNCH_EMAIL_SUBJECT`** - Default: `'Thanks for signing up'` - Email subject
- **`HTK_PRELAUNCH_EMAIL_BCC`** - Default: `[]` - BCC email addresses
- **`HTK_PRELAUNCH_EARLY_ACCESS_EMAIL_TEMPLATE`** - Default: `'htk/prelaunch_early_access'` - Early access template
- **`HTK_PRELAUNCH_EARLY_ACCESS_EMAIL_SUBJECT`** - Default: `'Early Access Granted'` - Early access subject

### Admin Tools

- **`HTK_PRELAUNCH_ADMINTOOLS_TOGGLE_URL_NAME`** - Default: `'admintools_api_prelaunch_toggle'` - URL for admin toggle

## Usage Examples

### Enable Prelaunch Mode

```python
# In Django settings.py
HTK_PRELAUNCH_MODE = True
HTK_PRELAUNCH_TEMPLATE = 'myapp/prelaunch.html'
```

### Configure Host Restrictions

```python
# In Django settings.py
import re

HTK_PRELAUNCH_HOST_REGEXPS = [
    r'(dev|qa|alpha)\.example\.com',
    r'demo\.example\.com',
]
```

### Add View Exceptions

```python
# In Django settings.py
HTK_PRELAUNCH_EXCEPTION_VIEWS = (
    'htk_prelaunch',
    'htk_feedback_submit',
    'robots',
    'django.contrib.sitemaps.views.sitemap',
)
```

### Configure Custom Emails

```python
# In Django settings.py
HTK_PRELAUNCH_EMAIL_TEMPLATE = 'myapp/emails/prelaunch_confirmation.txt'
HTK_PRELAUNCH_EMAIL_SUBJECT = 'Welcome! You are now on the waiting list'
HTK_PRELAUNCH_EARLY_ACCESS_EMAIL_TEMPLATE = 'myapp/emails/early_access.txt'
```
