# Test Scaffold Constants

> Test environment configuration constants for Django test cases

## Purpose
This module provides constants used in HTK's test scaffolding system, including test server hostnames and test email domain configurations for creating test fixtures and mock data.

## Key Files
- `__init__.py` - Exports core test constants
- `defaults.py` - Default test configuration values

## Key Components / Features

### Test Server (`__init__.py`)
- `TESTSERVER` - Django test server hostname (value: 'testserver')

### Test Email Configuration (`defaults.py`)
- `HTK_TEST_EMAIL_DOMAIN` - Default domain for generating test email addresses (default: 'hacktoolkit.com')

## Usage

```python
from htk.test_scaffold.constants import TESTSERVER, HTK_TEST_EMAIL_DOMAIN
from django.test import TestCase

class UserTestCase(TestCase):
    def setUp(self):
        # Generate test email addresses
        self.test_email = f"testuser@{HTK_TEST_EMAIL_DOMAIN}"

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email=self.test_email,
            password='testpass123'
        )

    def test_user_email_domain(self):
        # Verify test email domain
        self.assertTrue(self.user.email.endswith(HTK_TEST_EMAIL_DOMAIN))

    def test_server_name(self):
        # Use TESTSERVER constant for assertions
        response = self.client.get('/api/endpoint/')
        self.assertEqual(response.wsgi_request.get_host(), TESTSERVER)

# Generate multiple test users
def create_test_users(count=10):
    users = []
    for i in range(count):
        email = f"user{i}@{HTK_TEST_EMAIL_DOMAIN}"
        user = User.objects.create_user(
            username=f'user{i}',
            email=email,
            password='testpass'
        )
        users.append(user)
    return users
```

## Related Modules
- Parent: `htk/test_scaffold/`
- Related:
  - `htk.test_scaffold.models` - Test model factories
  - `htk.test_scaffold.utils` - Test utility functions
  - Django's `django.test.TestCase` - Base test case class

## Notes
- Confidence: HIGH (>98%)
- Last Updated: November 2025
- Test email domain should be a domain you control or a known test domain
- TESTSERVER is Django's standard test server hostname
- Can be overridden in test settings for custom test environments
