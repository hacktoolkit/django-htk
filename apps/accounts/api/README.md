# API

REST API endpoints and views for this module.

## Overview

This API module provides REST API endpoints for programmatic access to the service. Endpoints support standard HTTP methods and return JSON responses.

## Quick Start

### Basic Request

```python
import requests

# Make API request
response = requests.get('https://api.example.com/endpoint/', auth=auth)
result = response.json()
```

### Authentication

API endpoints require authentication. Configure credentials:

```python
from requests.auth import HTTPBearerAuth

auth = HTTPBearerAuth(token='your_token')
response = requests.get('https://api.example.com/endpoint/', auth=auth)
```

## API Endpoints

### Available Endpoints

Check the `views.py` file for a complete list of available endpoints and their parameters.

### Request Format

```
METHOD /endpoint/ HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer <token>

{
  "param1": "value1",
  "param2": "value2"
}
```

### Response Format

Successful responses return HTTP 200 with JSON data.

Error responses include status code and error message.

## Common Operations

### Get Resource

```python
response = requests.get(
    'https://api.example.com/resource/{id}/',
    auth=auth
)
resource = response.json()
```

### Create Resource

```python
response = requests.post(
    'https://api.example.com/resource/',
    json={'field': 'value'},
    auth=auth
)
new_resource = response.json()
```

### Update Resource

```python
response = requests.patch(
    'https://api.example.com/resource/{id}/',
    json={'field': 'new_value'},
    auth=auth
)
updated = response.json()
```

### Delete Resource

```python
response = requests.delete(
    'https://api.example.com/resource/{id}/',
    auth=auth
)
# Returns 204 No Content on success
```

## Error Handling

```python
import requests
from requests.exceptions import RequestException

try:
    response = requests.get(endpoint, auth=auth)
    response.raise_for_status()
    data = response.json()
except requests.HTTPError as e:
    print(f"HTTP Error: {e.response.status_code}")
except RequestException as e:
    print(f"Request Error: {e}")
```

## Configuration

Configure API settings in Django settings:

```python
# settings.py
HTK_API_ENABLED = True
HTK_API_TIMEOUT = 30
HTK_API_MAX_RETRIES = 3
HTK_API_RATE_LIMIT = 1000
```

## Best Practices

1. **Handle errors** - Implement proper error handling for all requests
2. **Use pagination** - For list endpoints, use limit and offset parameters
3. **Add retries** - Implement exponential backoff for transient failures
4. **Cache responses** - Cache frequently accessed data when appropriate
5. **Validate input** - Validate request parameters before sending
6. **Log requests** - Log all API calls for debugging and monitoring
7. **Set timeouts** - Always set request timeouts to prevent hanging
