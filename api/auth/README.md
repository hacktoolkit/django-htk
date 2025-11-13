# API Authentication

HTTP Bearer token authentication for REST APIs.

## Quick Start

```python
from htk.api.auth import HTTPBearerAuth
from requests.auth import HTTPBearer

# Use with requests library
import requests

headers = {'Authorization': 'Bearer your_token_here'}
response = requests.get('https://api.example.com/data', headers=headers)

# Or use HTTPBearerAuth class
auth = HTTPBearerAuth(token='your_token_here')
response = requests.get('https://api.example.com/data', auth=auth)
```

## HTTPBearerAuth

Bearer token authentication for API calls:

```python
from htk.api.auth import HTTPBearerAuth

# Create bearer auth with token
auth = HTTPBearerAuth(token='abc123xyz')

# Use with any HTTP request
import requests
response = requests.get('https://api.example.com/users', auth=auth)

# Token automatically included in Authorization header
# Header sent: Authorization: Bearer abc123xyz
```

## Common Patterns

### API Client with Bearer Token

```python
from htk.api.auth import HTTPBearerAuth
import requests

class APIClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.auth = HTTPBearerAuth(token=token)

    def get(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, auth=self.auth)
        return response.json()

    def post(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=data, auth=self.auth)
        return response.json()

# Usage
client = APIClient('https://api.example.com', token='your_token')
users = client.get('users')
```

### Django REST Framework Integration

```python
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Request must include: Authorization: Bearer token_value
        return Response({'user': str(request.user)})
```

### Token Management

```python
from htk.api.auth import HTTPBearerAuth
import os

# Load token from environment
api_token = os.environ.get('API_TOKEN')
auth = HTTPBearerAuth(token=api_token)

# Rotate token by creating new auth instance
new_token = refresh_api_token()
auth = HTTPBearerAuth(token=new_token)
```

## Configuration

```python
# settings.py
API_TOKEN = os.environ.get('API_TOKEN')
API_BASE_URL = os.environ.get('API_BASE_URL', 'https://api.example.com')
```

## Best Practices

1. **Store tokens securely** - Use environment variables or secrets manager
2. **Never commit tokens** - Add to .gitignore and use environment variables
3. **Rotate tokens regularly** - Update tokens periodically for security
4. **Use HTTPS** - Always use HTTPS when sending Bearer tokens
5. **Include in request headers** - Format: `Authorization: Bearer <token>`

## Related Modules

- `htk.api` - General API utilities
- `htk.api.utils` - API helper functions
- `rest_framework.authentication` - Django REST authentication
