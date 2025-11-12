# HTK Middleware Module

> Django middleware for request handling, timing, validation, and user agent parsing.

## Purpose

The middleware module provides reusable Django middleware classes for common request-handling patterns including global request access, request timing, host validation, timezone handling, user agent parsing, and error handling.

## Quick Start

```python
# settings.py
MIDDLEWARE = [
    # ... other middleware
    'htk.middleware.classes.GlobalRequestMiddleware',
    'htk.middleware.classes.RequestTimerMiddleware',
    'htk.middleware.classes.AllowedHostsMiddleware',
    'htk.middleware.classes.TimezoneMiddleware',
    'htk.middleware.classes.UserAgentMiddleware',
    'htk.middleware.classes.HttpErrorResponseMiddleware',
    'htk.middleware.classes.RequestDataTooBigMiddleware',
    'htk.middleware.classes.RewriteJsonResponseContentTypeMiddleware',
]

# Access global request in views/utils
from htk.middleware.classes import GlobalRequestMiddleware

request = GlobalRequestMiddleware.get_current_request()
```

## Key Components

| Middleware | Purpose |
|-----------|---------|
| **GlobalRequestMiddleware** | Access request object globally (thread-safe) |
| **AllowedHostsMiddleware** | Validate and redirect invalid hosts |
| **RequestTimerMiddleware** | Measure request execution time |
| **TimezoneMiddleware** | Set timezone per request/user |
| **UserAgentMiddleware** | Parse and attach user agent details |
| **HttpErrorResponseMiddleware** | Custom handling for HTTP errors |
| **RequestDataTooBigMiddleware** | Handle oversized request data |
| **RewriteJsonResponseContentTypeMiddleware** | Fix JSON content-type headers |

## Common Patterns

### Global Request Access

```python
from htk.middleware.classes import GlobalRequestMiddleware
from django.http import JsonResponse

def my_utility_function():
    """Access request without passing it as parameter"""
    request = GlobalRequestMiddleware.get_current_request()
    if request:
        user = request.user
        return f"Logged in as {user.username}"
    return "No active request"

# Or use in view
def my_view(request):
    current_request = GlobalRequestMiddleware.get_current_request()
    assert current_request is request  # True
    return JsonResponse({'status': 'ok'})
```

### Request Timing and Monitoring

```python
from htk.middleware.classes import RequestTimerMiddleware

def log_slow_requests():
    """Use request timer data for monitoring"""
    # In signal handler or logging middleware
    timer = RequestTimerMiddleware.get_current_timer()
    if timer and timer.elapsed() > 1.0:  # Request took > 1 second
        logger.warning(f"Slow request: {timer.elapsed()} seconds")

# settings.py
MIDDLEWARE = [
    'htk.middleware.classes.RequestTimerMiddleware',
    # ... other middleware
]
```

### Host Validation and Redirects

```python
# settings.py
ALLOWED_HOST_REGEXPS = [
    r'^example\.com$',
    r'^www\.example\.com$',
    r'^api\.example\.com$',
    r'^localhost(:\d+)?$',
]
HTK_DEFAULT_DOMAIN = 'www.example.com'

# Middleware will:
# - Redirect invalid hosts to HTK_DEFAULT_DOMAIN
# - Strip trailing '.' from hostnames
# - Allow /health_check without validation
MIDDLEWARE = [
    'htk.middleware.classes.AllowedHostsMiddleware',
]
```

### Timezone per User

```python
# settings.py
MIDDLEWARE = [
    'htk.middleware.classes.TimezoneMiddleware',
]

# View
def timezone_test(request):
    # Timezone set from user's timezone preference
    from django.utils import timezone
    now = timezone.now()
    return JsonResponse({'timezone': str(timezone.get_current_timezone())})
```

### User Agent Detection

```python
from htk.middleware.classes import UserAgentMiddleware

def mobile_only_view(request):
    """Check if request is from mobile device"""
    if not request.user_agent.is_mobile:
        return JsonResponse({'error': 'Mobile only'}, status=403)

    return JsonResponse({
        'device': request.user_agent.device.family,
        'os': request.user_agent.os.family,
        'browser': request.user_agent.browser.family,
    })
```

## Configuration

### AllowedHostsMiddleware

```python
# settings.py
ALLOWED_HOST_REGEXPS = [
    r'^example\.com$',
    r'^www\.example\.com$',
]
HTK_DEFAULT_DOMAIN = 'www.example.com'
```

### TimezoneMiddleware

```python
# User model should have timezone field
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(
        max_length=63,
        choices=[(tz, tz) for tz in pytz.all_timezones],
        default='UTC'
    )
```

## Best Practices

- **Order matters** - Place GlobalRequestMiddleware early, HttpErrorResponseMiddleware late
- **Use sparingly** - GlobalRequest adds thread overhead; pass request explicitly when possible
- **Handle exceptions** - All middleware should gracefully handle missing request context
- **Test middleware independently** - Mock request objects and test state management
- **Monitor performance** - Use RequestTimer to identify slow requests

## Testing

```python
from django.test import TestCase, RequestFactory
from htk.middleware.classes import (
    GlobalRequestMiddleware,
    RequestTimerMiddleware,
)

class MiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.global_middleware = GlobalRequestMiddleware()
        self.timer_middleware = RequestTimerMiddleware()

    def test_global_request_storage(self):
        """GlobalRequestMiddleware stores request per thread"""
        request = self.factory.get('/')
        self.global_middleware.process_request(request)

        # Request is now globally accessible
        stored_request = GlobalRequestMiddleware.get_current_request()
        self.assertEqual(stored_request, request)

    def test_timer_tracks_elapsed_time(self):
        """RequestTimerMiddleware measures request duration"""
        request = self.factory.get('/')
        self.timer_middleware.process_request(request)

        # Simulate work
        import time
        time.sleep(0.1)

        timer = RequestTimerMiddleware.get_current_timer()
        self.assertGreater(timer.elapsed(), 0.1)
```

## Related Modules

- `htk.middleware.classes` - Middleware implementations
- `htk.middleware.session_keys` - Session key middleware
- `htk.utils.request` - Request utilities
- `htk.api.utils` - JSON response utilities

## References

- [Django Middleware Documentation](https://docs.djangoproject.com/en/stable/topics/http/middleware/)
- [Django MiddlewareMixin](https://docs.djangoproject.com/en/stable/topics/http/middleware/#writing-your-own-middleware)
- [Thread Safety in Django](https://docs.djangoproject.com/en/stable/topics/async/#async-safety)

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
