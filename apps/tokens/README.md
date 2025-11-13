# Tokens App

API token generation, validation, and management.

## Quick Start

```python
from htk.apps.tokens.models import AuthToken

# Create token for user
token = AuthToken.objects.create(
    user=user,
    token_string='abcd1234efgh5678',
    expiry_date=timezone.now() + timedelta(days=30)
)

# Validate token
valid = AuthToken.objects.filter(
    token_string=token_str,
    user=user,
    expiry_date__gt=timezone.now()
).exists()
```

## Common Patterns

```python
# Token authentication in views
@require_http_methods(['POST'])
def api_endpoint(request):
    token_str = request.headers.get('Authorization', '').replace('Bearer ', '')

    try:
        token = AuthToken.objects.get(
            token_string=token_str,
            expiry_date__gt=timezone.now()
        )
        user = token.user
    except AuthToken.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    # Process request for authenticated user
    return JsonResponse({'user_id': user.id})
```

## Models

- **`AuthToken`** - API token with expiration
- **`TokenMetadata`** - Store token metadata

## Security

```python
# Generate secure tokens
import secrets
token = secrets.token_urlsafe(32)

# Hash before storing
import hashlib
token_hash = hashlib.sha256(token.encode()).hexdigest()
```

## Best Practices

1. **Hash tokens** - Never store plaintext tokens
2. **Set expiration** - All tokens should expire
3. **Regenerate on compromise** - Allow users to revoke
4. **Log token usage** - Track API access
5. **Use HTTPS** - Tokens in transit must be encrypted
