# HTK Decorators Module

> Function and method decorators for common patterns (deprecation, rate limiting, Celery tasks).

## Purpose

The decorators module provides reusable function and method decorators for common patterns in web applications, including deprecation warnings, rate limiting, Celery task management, and session-based tracking.

## Quick Start

```python
from htk.decorators.classes import deprecated
from htk.decorators.celery_ import celery_task
from htk.decorators.rate_limiters import rate_limit

# Mark a function as deprecated
@deprecated(reason="Use new_function instead")
def old_function():
    return "old value"

# Create an async Celery task
@celery_task(queue='email')
def send_notification(user_id):
    # Implementation
    pass

# Rate limit an API endpoint
@rate_limit(limit=10, window=3600)  # 10 requests per hour
def api_endpoint(request):
    return JsonResponse({'status': 'ok'})
```

## Key Components

| Component | Purpose |
|-----------|---------|
| **deprecated** | Mark functions/methods as deprecated with warnings |
| **celery_task** | Wrap functions for async execution via Celery |
| **rate_limit** | Limit function calls per time window |
| **track_session_key** | Track/validate session state |

## Common Patterns

### Deprecation with Clear Migration Path

```python
from htk.decorators.classes import deprecated

class DataAPI:
    @deprecated(
        reason="Use fetch_data_v2() instead. See migration guide at /docs/api-v2",
        version="2.0",
        removal_date="2025-12-01"
    )
    def fetch_data(self, user_id):
        """Deprecated method - delegates to v2 implementation"""
        return self.fetch_data_v2(user_id)

    def fetch_data_v2(self, user_id, context=None):
        """New implementation with enhanced features"""
        # Implementation
        pass
```

### Async Celery Tasks with Retry Logic

```python
from htk.decorators.celery_ import celery_task

@celery_task(queue='notifications', priority=5)
def process_payment(order_id, retry_count=3):
    """Process payment asynchronously with retries"""
    try:
        order = Order.objects.get(id=order_id)
        payment_service.charge(order.amount)
    except PaymentError as e:
        if retry_count > 0:
            process_payment.delay(order_id, retry_count - 1)
        else:
            logger.error(f"Payment failed for order {order_id}")
```

### Rate Limiting with Custom Key Function

```python
from htk.decorators.rate_limiters import rate_limit
from django.core.cache import cache

def get_user_key(request):
    """Generate rate limit key based on user"""
    return f"api_calls:{request.user.id}"

@rate_limit(limit=100, window=3600, key_func=get_user_key)
def api_search(request):
    """Search API with per-user rate limiting"""
    query = request.GET.get('q')
    return JsonResponse({'results': search(query)})
```

### Session-Based Tracking for Security

```python
from htk.decorators.session_keys import track_session_key

@track_session_key('login_attempts')
def login(request):
    """Track login attempts in session"""
    attempts = request.session.get('login_attempts', 0) + 1
    request.session['login_attempts'] = attempts

    if attempts > 5:
        return JsonResponse({'error': 'Too many attempts'}, status=429)

    # Validate credentials and login user
    return JsonResponse({'status': 'logged in'})
```

## Configuration

### Rollbar Integration (for deprecation warnings)

```python
# settings.py
ROLLBAR = {
    'enabled': True,
    'access_token': 'your_rollbar_token',
    'environment': 'production',
}
```

### Celery Configuration

```python
# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
```

### Cache Configuration (for rate limiting)

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

## Best Practices

- **Deprecation strategy** - Always provide a migration path and removal date; redirect to new function
- **Async patterns** - Use Celery for long-running operations (email, image processing, external API calls)
- **Rate limiting** - Set appropriate limits based on use case; monitor actual usage to adjust
- **Session tracking** - Use for security-critical operations; validate state before processing
- **Decorator order** - Apply rate limiting before Celery decorator to avoid bypassing limits

## Testing

```python
from django.test import TestCase
import warnings

class DecoratorTestCase(TestCase):
    def test_deprecation_warning(self):
        """Verify deprecation warning is emitted"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            old_function()
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))

    def test_rate_limit_exceeded(self):
        """Test rate limiting enforcement"""
        for i in range(11):  # Limit is 10
            response = self.client.get('/api/endpoint/')
        self.assertEqual(response.status_code, 429)  # Too Many Requests
```

## Related Modules

- `htk.decorators.classes` - Decorator class definitions
- `htk.decorators.celery_` - Celery task integration
- `htk.decorators.rate_limiters` - Rate limiting decorators
- `htk.decorators.session_keys` - Session management decorators
- `htk.utils.log` - Logging utilities

## References

- [Python Functools](https://docs.python.org/3/library/functools.html)
- [Python Deprecation Warnings](https://docs.python.org/3/library/warnings.html)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Django Cache Framework](https://docs.djangoproject.com/en/stable/topics/cache/)

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
