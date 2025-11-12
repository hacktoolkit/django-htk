# HTK Test Scaffold Module

> Comprehensive testing utilities, base test cases, and test data generation for Django applications

## Purpose

The `test_scaffold` module provides a complete testing framework for Django applications, including base test case classes with built-in fixtures and helper methods, test data generation utilities for creating realistic test users and credentials, fake time and prelaunch mode management for controlled test environments, and HTTP request helpers with assertion utilities.

## Directory Structure

```
test_scaffold/
├── __init__.py                  # Module initialization
├── models.py                    # Test models (FakeTime, FakePrelaunch, TestScaffold)
├── utils.py                     # Test data generation utilities
├── test_data.py                 # Test data constants
├── tests.py                     # Base test case classes
├── apps.py                      # Django app configuration
└── constants/
    └── README.md                # [See constants/README.md](constants/README.md)
```

## Subdirectories

### [constants/](constants/README.md) - Test Scaffold Constants
Test environment configuration constants including Django test server hostname (`TESTSERVER`) and test email domain configuration (`HTK_TEST_EMAIL_DOMAIN`).

## Key Components

### Test Models

**FakeTime** (models.py)
- Single-record model storing a timestamp for mocking system time in tests
- Allows tests to control and assert on time-dependent logic
- Methods: `set_fake_timestamp()`, `get_fake_timestamp()`, `clear_fake_timestamp()`

**FakePrelaunch** (models.py)
- Single-record model storing prelaunch mode flags
- Supports two boolean fields: `prelaunch_mode` and `prelaunch_host`
- Used to test conditional prelaunch redirects and features

**TestScaffold** (models.py)
- Utility class managing FakeTime and FakePrelaunch records
- All methods are class methods for convenient access
- Methods: `set_fake_timestamp()`, `get_fake_timestamp()`, `clear_fake_timestamp()`, `set_fake_prelaunch()`, `get_fake_prelaunch_mode()`, `get_fake_prelaunch_host()`, `clear_fake_prelaunch()`

### Test Data Generation

**Test User Creation** (utils.py)
- `create_test_user()` - Creates a Django user with optional email/name and email association
- `create_test_user_with_email_and_password()` - Creates user with email and password; returns (user, email, password) tuple
- `create_test_email()` - Generates unique test email with random hex suffix and configurable domain
- `create_test_username()` - Generates random username with "test_" prefix and UUID hex
- `create_test_password()` - Generates random password using UUID hex
- `get_test_display_name()` - Returns random display name from predefined list + random number
- `get_test_username()` - Returns random username from predefined list + random number
- `get_random_string()` - Creates random string with optional max length constraint

**Test Data Constants** (test_data.py)
```python
TEST_DISPLAY_NAMES = [
    'Jose Sanchez', 'Don Juan', 'Miles George', 'Pablo Sandoval',
    'Leonardo Davinci', 'Tom Hanks', 'Ricardo Lopez', 'Ernesto Guerillo',
    'Michaelangelo Turtle', 'Rafael Donatello'
]

TEST_USERNAMES = [
    'graffiti4evr', 'captobvious', 'mrfoo', 'mrbar'
]
```

### Base Test Cases

**BaseTestCase** (tests.py)
- Foundation test case with fixture loading and user batch management
- `setUp()` automatically creates 5 test users for use in tests
- Methods:
  - `_create_batch_test_users()` - Creates batch of test users
  - `_assign_test_user()` - Returns next unassigned user; creates more if needed
- Uses `initial_data` fixtures for database setup

**BaseWebTestCase** (tests.py)
- Extends BaseTestCase with HTTP request helpers and web testing utilities
- Prelaunch mode automatically disabled in setUp
- HTTP request methods:
  - `_get(view_name, args=None, kwargs=None, data=None)` - Perform GET request
  - `_post(view_name, data, ...)` - Perform POST request
  - `_put(view_name, data, ...)` - Perform PUT request
  - `_delete(view_name, args=None, kwargs=None)` - Perform DELETE request
- User session helpers:
  - `_get_user_session()` - Returns (user, password, client) for authenticated requests
  - `_get_user_session_with_primary_email()` - Returns user with primary email + auth credentials
- Response assertions:
  - `_check_view_is_okay(response)` - Assert HTTP 200
  - `_check_view_404(response)` - Assert HTTP 404
  - `_check_view_does_not_exist(response)` - Assert HTTP 404
  - `_check_response_redirect_chain(response, expected_path, secure=False)` - Validate redirect chain
  - `_check_view_redirects_to_another(response, expected_full_uri)` - Assert redirect to specific URI
  - `_check_view_redirects_to_login(response, next_url)` - Assert redirect to login
- Prelaunch mode checker:
  - `_check_prelaunch_mode(response, prelaunch_mode)` - Assert prelaunch mode in response

## Usage Examples

### Creating Test Users

```python
from htk.test_scaffold.utils import (
    create_test_user,
    create_test_email,
    create_test_username,
    create_test_password,
    create_test_user_with_email_and_password,
)

# Create simple test user
user = create_test_user()

# Create user with email
email = create_test_email()
user = create_test_user(email=email)

# Create user with full credentials
user, email, password = create_test_user_with_email_and_password()

# Generate test credentials separately
test_email = create_test_email()
test_username = create_test_username()
test_password = create_test_password()
```

### Using BaseTestCase

```python
from django.test import TestCase
from htk.test_scaffold.tests import BaseTestCase

class UserServiceTestCase(BaseTestCase):
    """Test case with automatic test user setup"""

    def test_user_creation(self):
        """Test creating a user"""
        # _assign_test_user() returns next available test user
        user = self._assign_test_user()
        self.assertEqual(user.username, user.username)  # Verify user exists

    def test_batch_user_operations(self):
        """Test operations on multiple users"""
        # Get multiple test users
        users = [self._assign_test_user() for _ in range(3)]
        self.assertEqual(len(users), 3)
        self.assertTrue(all(u.id for u in users))
```

### Using BaseWebTestCase for API Testing

```python
from django.test import TestCase
from htk.test_scaffold.tests import BaseWebTestCase

class UserAPITestCase(BaseWebTestCase):
    """Test case with HTTP request helpers"""

    def test_get_user_profile(self):
        """Test GET user profile API endpoint"""
        user, password, client = self._get_user_session()

        # Make authenticated GET request
        response = self._get('api-user-profile', kwargs={'user_id': user.id})

        # Assert response is OK
        self._check_view_is_okay(response)

        # Verify response data
        data = response.json()
        self.assertEqual(data['username'], user.username)

    def test_update_user_profile(self):
        """Test POST to update user profile"""
        user, password, client = self._get_user_session()

        # Update user data
        data = {'bio': 'Updated bio', 'location': 'New York'}
        response = self._post('api-user-update', data, kwargs={'user_id': user.id})

        # Assert successful update
        self._check_view_is_okay(response)

    def test_delete_user(self):
        """Test DELETE user endpoint"""
        user, password, client = self._get_user_session()

        response = self._delete('api-user-delete', kwargs={'user_id': user.id})

        # Assert successful deletion
        self._check_view_is_okay(response)
```

### Using BaseWebTestCase for Web Testing

```python
from django.test import TestCase
from htk.test_scaffold.tests import BaseWebTestCase

class UserAuthTestCase(BaseWebTestCase):
    """Test authentication views and redirects"""

    def test_login_redirect(self):
        """Test that unauthenticated users are redirected to login"""
        response = self._get('user-dashboard')

        # Should redirect to login
        next_url = '/accounts/login/'
        self._check_view_redirects_to_login(response, next_url)

    def test_authenticated_access(self):
        """Test authenticated user can access protected view"""
        user, password, client = self._get_user_session()

        # Make request to protected view
        response = self._get('user-dashboard')

        # Should return 200 OK
        self._check_view_is_okay(response)

    def test_permission_denied(self):
        """Test user without permission gets 404"""
        user, password, client = self._get_user_session()

        # Try to access admin-only view
        response = self._get('admin-users')

        # Should get 404 or 403
        self._check_view_404(response)
```

### Managing Fake Time

```python
from django.test import TestCase
from datetime import datetime, timedelta
from htk.test_scaffold.models import TestScaffold

class TimeBasedTestCase(TestCase):
    """Test time-dependent logic"""

    def test_expired_token(self):
        """Test token expiration logic"""
        # Set fake time to specific moment
        target_time = datetime(2024, 1, 1, 12, 0, 0)
        TestScaffold.set_fake_timestamp(target_time)

        # Create token at this time
        token = create_token()
        self.assertTrue(token.is_valid())

        # Advance time to after expiration
        expired_time = target_time + timedelta(hours=25)
        TestScaffold.set_fake_timestamp(expired_time)

        # Token should now be expired
        self.assertFalse(token.is_valid())

        # Clean up
        TestScaffold.clear_fake_timestamp()
```

### Managing Prelaunch Mode

```python
from django.test import TestCase
from htk.test_scaffold.models import TestScaffold

class PrelaunchFeatureTestCase(TestCase):
    """Test prelaunch-gated features"""

    def test_feature_available_after_launch(self):
        """Test feature is available when prelaunch mode is off"""
        # Ensure prelaunch is disabled
        TestScaffold.set_fake_prelaunch(prelaunch_mode=False)

        response = self.client.get('/feature/')
        self.assertEqual(response.status_code, 200)

        TestScaffold.clear_fake_prelaunch()

    def test_feature_hidden_during_prelaunch(self):
        """Test feature is hidden during prelaunch"""
        # Enable prelaunch mode
        TestScaffold.set_fake_prelaunch(prelaunch_mode=True)

        response = self.client.get('/feature/')
        # Should redirect or return 404
        self.assertIn(response.status_code, [301, 302, 404])

        TestScaffold.clear_fake_prelaunch()
```

## Test Patterns

### Pattern 1: Testing Model Methods

```python
from htk.test_scaffold.tests import BaseTestCase
from myapp.models import Product

class ProductTestCase(BaseTestCase):
    """Test Product model methods"""

    def test_product_discount_calculation(self):
        """Test discount calculation"""
        user = self._assign_test_user()
        product = Product.objects.create(
            name='Test Product',
            price=100.00,
            discount=10,  # 10% discount
        )

        discounted_price = product.get_discounted_price()
        self.assertEqual(discounted_price, 90.00)
```

### Pattern 2: Testing View Behavior

```python
from htk.test_scaffold.tests import BaseWebTestCase

class CheckoutViewTestCase(BaseWebTestCase):
    """Test checkout view with authenticated user"""

    def test_checkout_flow(self):
        """Test complete checkout flow"""
        user, password, client = self._get_user_session()

        # Step 1: View cart
        response = self._get('cart-view', client=client)
        self._check_view_is_okay(response)

        # Step 2: Initiate checkout
        response = self._post('checkout-start', {'items': [1, 2, 3]}, client=client)
        self._check_view_is_okay(response)

        # Step 3: Confirm payment
        payment_data = {'card_token': 'tok_visa', 'amount': 150.00}
        response = self._post('checkout-confirm', payment_data, client=client)
        self._check_view_is_okay(response)
```

### Pattern 3: Testing Multiple Users

```python
from htk.test_scaffold.tests import BaseWebTestCase

class MultiUserFeatureTestCase(BaseWebTestCase):
    """Test features involving multiple users"""

    def test_user_following(self):
        """Test user follow/unfollow functionality"""
        follower = self._assign_test_user()
        followee = self._assign_test_user()

        # Follower follows followee
        client = Client()
        client.force_login(follower)
        response = self._post('user-follow', {'user_id': followee.id}, client=client)
        self._check_view_is_okay(response)

        # Verify follow relationship
        self.assertTrue(
            follower.profile.following.filter(id=followee.id).exists()
        )
```

## Best Practices

1. **Extend Base Test Cases**
   - Always inherit from `BaseTestCase` or `BaseWebTestCase`
   - Don't reinvent test setup and assertion helpers

2. **Use Test Data Generation**
   - Use `create_test_user()` and related functions instead of hardcoding test data
   - Ensures consistent, randomized test data

3. **Leverage Batch User Pool**
   - Use `_assign_test_user()` to get pre-created test users
   - More efficient than creating new users for each test

4. **Use HTTP Helpers**
   - Use `_get()`, `_post()`, etc. instead of manual URL reversal
   - Use response assertion methods for consistent validation

5. **Test Authentication**
   - Use `_get_user_session()` for authenticated requests
   - Test both authenticated and unauthenticated scenarios

6. **Manage Time and Prelaunch State**
   - Use `TestScaffold` methods to control time in time-dependent tests
   - Clean up state with `clear_*` methods

## Configuration

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'htk.test_scaffold',
    # ...
]

# Test data configuration (optional)
HTK_TEST_EMAIL_DOMAIN = 'hacktoolkit.com'
HTK_TEST_BATCH_SIZE = 5
HTK_TEST_BATCH_AUTO_CREATE = True
```

## Testing Overview

```
Test Environment Setup:
├── Fixtures load initial data (initial_data fixture)
├── BaseTestCase creates batch of 5 test users
├── BaseWebTestCase disables prelaunch mode
└── Each test can request authenticated sessions

Test Data Creation Flow:
1. create_test_email() → test+{uuid10}@hacktoolkit.com
2. create_test_username() → test_{uuid10}
3. create_test_password() → random UUID-based password
4. create_test_user() → User instance with optional email
5. Full setup → (user, email, password) tuple
```

## Related Modules

- `htk.models` - User profile and base models
- `htk.cache` - Caching system
- `htk.constants` - Application-wide constants
- Django test framework - Base TestCase and testing utilities

## API Reference

### TestScaffold Class Methods

```python
@classmethod
def set_fake_timestamp(dt=None, timestamp=None):
    """Mock system time with datetime or Unix timestamp"""

@classmethod
def get_fake_timestamp():
    """Retrieve current mocked timestamp"""

@classmethod
def clear_fake_timestamp():
    """Clear mocked timestamp"""

@classmethod
def set_fake_prelaunch(prelaunch_mode=False, prelaunch_host=False):
    """Set prelaunch flags"""

@classmethod
def get_fake_prelaunch_mode():
    """Get prelaunch mode boolean"""

@classmethod
def get_fake_prelaunch_host():
    """Get prelaunch host boolean"""

@classmethod
def clear_fake_prelaunch():
    """Clear prelaunch settings"""
```

### BaseWebTestCase HTTP Methods

```python
def _get(view_name, args=None, kwargs=None, data=None, secure=False, client=None):
    """Perform GET request with URL reversal"""

def _post(view_name, data, args=None, kwargs=None, secure=False, client=None):
    """Perform POST request with URL reversal"""

def _put(view_name, data, args=None, kwargs=None, secure=False, client=None):
    """Perform PUT request with URL reversal"""

def _delete(view_name, args=None, kwargs=None, secure=False, client=None):
    """Perform DELETE request with URL reversal"""

def _get_user_session():
    """Returns (user, password, client) for authenticated requests"""

def _get_user_session_with_primary_email():
    """Returns user with primary email + auth credentials"""
```

### BaseWebTestCase Assertion Methods

```python
def _check_view_is_okay(response):
    """Assert HTTP 200 response"""

def _check_view_404(response):
    """Assert HTTP 404 response"""

def _check_view_does_not_exist(response):
    """Assert HTTP 404 response"""

def _check_response_redirect_chain(response, expected_path, secure=False):
    """Validate redirect chain matches expected path"""

def _check_view_redirects_to_another(response, expected_full_uri):
    """Assert redirect to specific full URI"""

def _check_view_redirects_to_login(response, next_url):
    """Assert redirect to login with next parameter"""

def _check_prelaunch_mode(response, prelaunch_mode):
    """Assert prelaunch mode status in response"""
```

## References

- [Django Testing Framework](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Django Test Client](https://docs.djangoproject.com/en/stable/topics/testing/tools/#client)
- [Django Database Fixtures](https://docs.djangoproject.com/en/stable/howto/initial-data/)

## Notes

- Confidence: **HIGH** (>98%) - Clear framework structure and patterns from code analysis
- Last Updated: November 2025
- Maintained by: HTK Contributors
