# HTK API Module

> REST/JSON API utilities, response helpers, and authentication backends.

## Purpose

The API module provides utilities for building JSON/REST APIs: response helpers for consistent formatting, authentication backends for token-based auth, and base classes to reduce boilerplate.

## Quick Start

```python
from htk.api.utils import json_response_okay, json_response_error
from django.views import View

class UserAPIView(View):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            return json_response_okay({
                'id': user.id,
                'username': user.username,
                'email': user.email,
            })
        except User.DoesNotExist:
            return json_response_error('User not found', status=404)
```

## Key Components

| Component | Purpose |
|-----------|---------|
| **json_response()** | Generate JSON responses with custom status |
| **json_response_okay()** | Generate 200 OK JSON responses |
| **json_response_error()** | Generate error JSON responses |
| **HtkUserTokenAuthBackend** | Token-based authentication for APIs |

## Common Patterns

### JSON Responses

```python
from htk.api.utils import json_response_okay, json_response_error

# Success
return json_response_okay({'id': user.id, 'name': user.name})

# Error with code
return json_response_error(
    'Invalid email',
    error_code='INVALID_EMAIL',
    status=400
)
```

### Pagination

```python
def api_list_items(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))

    queryset = Item.objects.all()
    total = queryset.count()
    start = (page - 1) * per_page
    items = queryset[start:start + per_page]

    return json_response_okay({
        'items': [{'id': i.id, 'name': i.name} for i in items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
        }
    })
```

### Token-Based Authentication

```python
from htk.apps.accounts.backends import HtkUserTokenAuthBackend

def authenticated_api(request):
    token = request.GET.get('token') or \
            request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')

    if not token:
        return json_response_error('No token', status=401)

    auth = HtkUserTokenAuthBackend()
    user = auth.authenticate(request, token=token)

    if not user:
        return json_response_error('Invalid token', status=401)

    return json_response_okay({
        'user_id': user.id,
        'username': user.username
    })
```

### Filtering and Sorting

```python
def api_search(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', 'name')
    order = request.GET.get('order', 'asc')

    queryset = Item.objects.filter(name__icontains=query)
    if order == 'desc':
        sort_by = f'-{sort_by}'
    queryset = queryset.order_by(sort_by)

    items = [{'id': i.id, 'name': i.name} for i in queryset]
    return json_response_okay({'items': items})
```

## Response Format

**Success:**
```json
{
  "status": "ok",
  "data": {
    "id": 1,
    "name": "Example"
  }
}
```

**Error:**
```json
{
  "status": "error",
  "message": "Item not found",
  "error_code": "NOT_FOUND"
}
```

## Configuration

Add to `urls.py`:

```python
from django.urls import path
from myapp.api import UserAPIView

urlpatterns = [
    path('api/users/<int:user_id>/', UserAPIView.as_view()),
]
```

## Best Practices

- **Consistent format** - All responses use same structure with status, message, data
- **Proper HTTP status codes** - 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found
- **Token authentication** - Use Bearer token header: `Authorization: Bearer <token>`
- **Error codes** - Include machine-readable error codes for client handling
- **Pagination** - Always include total count and page info for large datasets
- **CORS headers** - Set appropriate headers if serving cross-origin requests

## Testing

```python
from django.test import TestCase, Client
import json

class APITestCase(TestCase):
    def test_get_user(self):
        """Test getting user via API."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        response = self.client.get(f'/api/users/{user.id}/')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['data']['id'], user.id)
```

## Related Modules

- `htk.api.utils` - Response and formatting utilities
- `htk.api.views` - Base API view classes
- `htk.api.auth` - Authentication utilities
- `htk.apps.accounts.backends` - User authentication
- `htk.utils.http` - HTTP status helpers

## References

- [Django HttpResponse](https://docs.djangoproject.com/en/stable/ref/request-response/)
- [REST API Best Practices](https://restfulapi.net/)
- [Django Class-Based Views](https://docs.djangoproject.com/en/stable/topics/class-based-views/)

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
