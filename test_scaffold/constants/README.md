# Test Scaffold Constants

## Overview

This module provides configuration constants for test environment setup and test data generation.

## Constants

```python
from htk.test_scaffold.constants import TESTSERVER, HTK_TEST_EMAIL_DOMAIN

# Django test server hostname
TESTSERVER = 'testserver'

# Domain to use for test email addresses
HTK_TEST_EMAIL_DOMAIN = 'hacktoolkit.com'
```

## Usage Examples

### Generate Test Email

```python
from htk.test_scaffold.constants import HTK_TEST_EMAIL_DOMAIN

def create_test_user(username):
    """Create a test user with a test domain email."""
    email = f"{username}@{HTK_TEST_EMAIL_DOMAIN}"
    # Create user with email
    return email
```

### Test Server Validation

```python
from htk.test_scaffold.constants import TESTSERVER

def is_test_environment(request):
    """Check if running on test server."""
    return request.get_host().startswith(TESTSERVER)
```

## Customization

Override these settings in test settings.py:

```python
HTK_TEST_EMAIL_DOMAIN = 'test.local'
```
