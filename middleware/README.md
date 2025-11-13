# Middleware

## Overview

The `middleware` module provides utilities for:

- Global request access
- Request timing and profiling
- User agent parsing
- Host validation
- Error handling
- Timezone detection

## Global Request Access

Access request anywhere in your code without passing it explicitly:

```python
from htk.middleware.classes import GlobalRequestMiddleware
from htk.middleware.utils import get_current_request

# Enable in settings.py
MIDDLEWARE = [
    'htk.middleware.classes.GlobalRequestMiddleware',
    # ...
]

# Access request globally
def some_function():
    request = get_current_request()
    user = request.user
    host = request.get_host()
```

**Use Cases:**
- Access request in utility functions
- Log request context in debugging
- Track request metadata

## User Agent Parsing

Automatically parse and expose user agent info:

```python
from htk.middleware.classes import UserAgentMiddleware

# Enable in settings.py
MIDDLEWARE = [
    'htk.middleware.classes.UserAgentMiddleware',
    # ...
]

# Access in views
def my_view(request):
    user_agent = request.user_agent
    # {
    #   'is_mobile': True/False,
    #   'is_bot': True/False,
    #   'browser': 'Chrome',
    #   'os': 'Windows',
    #   'device': 'Desktop',
    # }
```

## Request Timing

Measure request processing time:

```python
from htk.middleware.classes import RequestTimerMiddleware

# Enable in settings.py
MIDDLEWARE = [
    'htk.middleware.classes.RequestTimerMiddleware',
    # ...
]

# View processing time in response headers
# X-Request-Time: 0.234 seconds
```

**Useful for:**
- Performance monitoring
- Identifying slow views
- A/B testing performance
- APM integration

## Host Validation

Validate requests against allowed hosts:

```python
from htk.middleware.classes import AllowedHostsMiddleware

# settings.py
ALLOWED_HOST_REGEXPS = [
    r'^example\.com$',
    r'^subdomain\.example\.com$',
    r'^localhost$',
]

# Enable middleware
MIDDLEWARE = [
    'htk.middleware.classes.AllowedHostsMiddleware',
    # ...
]
```

## Error Handling

Gracefully handle custom HTTP errors:

```python
from htk.middleware.classes import HttpErrorResponseMiddleware
from htk.utils.http.errors import HttpErrorResponseError

# Enable in settings.py
MIDDLEWARE = [
    'htk.middleware.classes.HttpErrorResponseMiddleware',
    # ...
]

# Raise errors in views
def api_endpoint(request):
    if not request.user.is_authenticated:
        raise HttpErrorResponseError(401, 'Unauthorized')
    # ...

# Middleware catches and formats response
# Returns: {'error': 'Unauthorized'} with 401 status
```

## JSON Content-Type Handling

Fix JSON response content type for IE compatibility:

```python
from htk.middleware.classes import RewriteJsonResponseContentTypeMiddleware

# Enable in settings.py
MIDDLEWARE = [
    'htk.middleware.classes.RewriteJsonResponseContentTypeMiddleware',
    # ...
]

# Ensures application/json content type (not text/html)
```

## Timezone Detection

Auto-detect and set user timezone:

```python
from htk.middleware.classes import TimezoneMiddleware

# Enable in settings.py
MIDDLEWARE = [
    'htk.middleware.classes.TimezoneMiddleware',
    # ...
]

# Automatically detects timezone from IP or user profile
# Sets timezone for datetime operations
```

## Request Data Limits

Prevent overly large requests:

```python
from htk.middleware.classes import RequestDataTooBigMiddleware

# Enable in settings.py
MIDDLEWARE = [
    'htk.middleware.classes.RequestDataTooBigMiddleware',
    # ...
]

# Returns 413 Payload Too Large if request exceeds limit
```

## Complete Example

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # HTK middleware
    'htk.middleware.classes.GlobalRequestMiddleware',
    'htk.middleware.classes.UserAgentMiddleware',
    'htk.middleware.classes.RequestTimerMiddleware',
    'htk.middleware.classes.TimezoneMiddleware',
    'htk.middleware.classes.AllowedHostsMiddleware',
    'htk.middleware.classes.RewriteJsonResponseContentTypeMiddleware',
    'htk.middleware.classes.HttpErrorResponseMiddleware',
    'htk.middleware.classes.RequestDataTooBigMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ALLOWED_HOST_REGEXPS = [
    r'^example\.com$',
    r'^www\.example\.com$',
]
```

## Best Practices

1. **Order matters** - Place middleware in logical order
2. **Global request** - Use sparingly, not a replacement for passing request
3. **Timezone handling** - Configure with user locale data
4. **Error responses** - Use HttpErrorResponseError for API errors
5. **Performance** - Monitor with RequestTimerMiddleware

## Classes

- **`GlobalRequestMiddleware`** - Store request in thread-local storage
- **`UserAgentMiddleware`** - Parse and expose user agent data
- **`RequestTimerMiddleware`** - Measure request processing time
- **`AllowedHostsMiddleware`** - Validate host against regex patterns
- **`HttpErrorResponseMiddleware`** - Handle custom HTTP errors
- **`RewriteJsonResponseContentTypeMiddleware`** - Fix JSON content type
- **`TimezoneMiddleware`** - Auto-detect user timezone
- **`RequestDataTooBigMiddleware`** - Enforce request size limits
