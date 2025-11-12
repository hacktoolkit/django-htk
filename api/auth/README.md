# HTK API Auth Module

> Authentication helpers for external API requests using the requests library.

## Purpose

The api.auth module provides authentication classes and utilities for making authenticated HTTP requests to external APIs using the Python `requests` library.

## Quick Start

```python
from htk.api.auth.requests import HTTPBearerAuth
import requests

# Make authenticated API request
token = 'your_api_token'
auth = HTTPBearerAuth(token)

response = requests.get(
    'https://api.example.com/users',
    auth=auth
)

# Bearer token automatically added to Authorization header
# GET /users HTTP/1.1
# Authorization: Bearer your_api_token
```

## Key Components

| Component | Purpose |
|-----------|---------|
| **HTTPBearerAuth** | Add Bearer token authentication to requests |

## Common Patterns

### Bearer Token Authentication

```python
from htk.api.auth.requests import HTTPBearerAuth
import requests

# Single request with token
token = 'sk_live_xyz123'
auth = HTTPBearerAuth(token)

response = requests.post(
    'https://api.example.com/charges',
    json={'amount': 2000, 'currency': 'usd'},
    auth=auth
)

if response.status_code == 200:
    print(f"Charge created: {response.json()['id']}")
else:
    print(f"Error: {response.json()['error']}")
```

### Reusable Session with Auth

```python
from htk.api.auth.requests import HTTPBearerAuth
import requests

# Create session with persistent auth
token = 'your_api_token'
session = requests.Session()
session.auth = HTTPBearerAuth(token)

# All requests in session automatically include bearer token
users = session.get('https://api.example.com/users').json()
account = session.get('https://api.example.com/account').json()
```

### With Error Handling

```python
from htk.api.auth.requests import HTTPBearerAuth
import requests
from requests.exceptions import RequestException

def call_api(endpoint, token, **kwargs):
    """Make authenticated API call with error handling"""
    try:
        auth = HTTPBearerAuth(token)
        response = requests.get(
            f'https://api.example.com{endpoint}',
            auth=auth,
            timeout=10,
            **kwargs
        )
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logger.error(f"API request failed: {e}")
        return None

# Usage
data = call_api('/users/123', token)
```

## Best Practices

- **Store tokens securely** - Use environment variables or secrets manager, never commit to code
- **Use sessions for multiple requests** - Reuse authenticated session to avoid recreating auth object
- **Add timeout** - Always specify timeout to prevent hanging requests
- **Handle errors gracefully** - Check status codes and catch request exceptions
- **Rotate tokens regularly** - Implement token rotation for security-critical APIs

## Testing

```python
from django.test import TestCase
from unittest.mock import patch, Mock
from htk.api.auth.requests import HTTPBearerAuth
import requests

class APIAuthTestCase(TestCase):
    def test_bearer_auth_header(self):
        """HTTPBearerAuth adds Bearer token to request"""
        token = 'test_token_123'
        auth = HTTPBearerAuth(token)

        # Create mock request
        request = Mock()
        request.headers = {}

        # Apply auth
        result = auth(request)

        # Verify header added
        self.assertEqual(result.headers['Authorization'], 'Bearer test_token_123')

    @patch('requests.get')
    def test_authenticated_request(self, mock_get):
        """Test making authenticated request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 1, 'name': 'Test'}
        mock_get.return_value = mock_response

        token = 'test_token'
        auth = HTTPBearerAuth(token)
        response = requests.get('https://api.example.com/users/1', auth=auth)

        self.assertEqual(response.json()['name'], 'Test')
```

## Related Modules

- `htk.api.utils` - JSON response utilities
- `htk.api.views` - API view classes
- `htk.utils.http` - HTTP utilities

## References

- [Requests Library Documentation](https://docs.python-requests.org/)
- [Requests Authentication](https://docs.python-requests.org/en/latest/user/authentication/)
- [OAuth 2.0 Bearer Token Usage](https://tools.ietf.org/html/rfc6750)

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
