# HTTP Utilities

HTTP response headers and error handling.

## Quick Start

```python
from htk.utils.http.response import set_cache_headers, set_cors_headers_for_image
from htk.utils.http.errors import HttpErrorResponseError

# Set cache headers on response
response = HttpResponse('content')
set_cache_headers(response, max_age=3600)

# Set CORS headers for images
set_cors_headers_for_image(response)
```

## Common Patterns

```python
# Create cacheable response
def get_cached_image(request):
    response = serve_image()
    set_cache_headers(response, max_age=86400)  # 1 day
    set_cors_headers_for_image(response)
    return response

# Handle HTTP errors
try:
    result = api_call()
except HttpErrorResponseError as e:
    return error_response(e.status_code)
```
