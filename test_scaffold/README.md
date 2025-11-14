# Test Scaffold

Base classes and utilities for testing.

## Quick Start

```python
from htk.test_scaffold.tests import BaseTestCase, BaseWebTestCase
from htk.test_scaffold.utils import create_test_user, create_test_username

class MyTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = create_test_user()

    def test_something(self):
        self.assertIsNotNone(self.user)
```

## Base Test Cases

### BaseTestCase

Base class for all tests with common setup:

```python
from htk.test_scaffold.tests import BaseTestCase

class ArticleTestCase(BaseTestCase):
    def test_article_creation(self):
        # Basic test methods
        self.assertIsNotNone(article)
```

### BaseWebTestCase

Extended base for web/integration tests:

```python
from htk.test_scaffold.tests import BaseWebTestCase

class ArticleWebTestCase(BaseWebTestCase):
    def test_article_view(self):
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)
```

## Utilities

### User Creation

```python
from htk.test_scaffold.utils import create_test_user, create_test_username

# Create test user with random username
user = create_test_user()
username = user.username  # auto-generated

# Generate random username
username = create_test_username()
```

## Fake Time

Mock system time for testing time-dependent features:

```python
from htk.test_scaffold.models import set_fake_timestamp
from datetime import datetime

# Set fake timestamp
fake_time = datetime(2024, 1, 1, 12, 0, 0)
set_fake_timestamp(fake_time)

# Your test runs with fake time
# Reset in tearDown
```

## Fake Prelaunch

Mock prelaunch status:

```python
from htk.test_scaffold.models import FakePrelaunch

# Set prelaunch mode
prelaunch = FakePrelaunch.objects.create(is_enabled=True)
```

## Common Patterns

### Testing with Test Users

```python
from htk.test_scaffold.tests import BaseTestCase
from htk.test_scaffold.utils import create_test_user

class UserAuthTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = create_test_user()
        self.admin = create_test_user()

    def test_user_login(self):
        self.client.login(
            username=self.user.username,
            password='password'
        )
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
```

### Testing Time-Dependent Logic

```python
from htk.test_scaffold.tests import BaseTestCase
from htk.test_scaffold.models import set_fake_timestamp
from datetime import datetime

class TimeBasedTestCase(BaseTestCase):
    def test_expiration(self):
        # Set time to before expiration
        set_fake_timestamp(datetime(2024, 1, 1))
        self.assertTrue(offer.is_valid())

        # Move time forward
        set_fake_timestamp(datetime(2024, 2, 1))
        self.assertFalse(offer.is_valid())
```

## Best Practices

1. **Extend BaseTestCase** for all tests
2. **Use create_test_user()** for test users
3. **Set up in setUp()** method
4. **Tear down in tearDown()** method
5. **Use fake time** for time-sensitive tests
