# URL Shortener App

Create and manage short URLs with base62 encoding.

## Quick Start

```python
from htk.apps.url_shortener.models import HTKShortUrl

# Create short URL
short = HTKShortUrl.objects.create(
    url='https://example.com/very/long/url?param=value'
)

code = short.code  # e.g., 'a7f2'
# Share as: example.com/s/a7f2

# Get original URL
short = HTKShortUrl.objects.get(code='a7f2')
original = short.url
```

## Models

- **`HTKShortUrl`** - Short URL with base62 encoded code

## Common Patterns

```python
# Generate short URL code
from htk.apps.url_shortener.utils import generate_short_url_code

code = generate_short_url_code(short.id)

# Get recently shortened
from htk.apps.url_shortener.utils import get_recently_shortened

recent = get_recently_shortened(limit=10)

# Resolve raw ID
from htk.apps.url_shortener.utils import resolve_raw_id

raw_id = resolve_raw_id('a7f2')
```

## URL Pattern

```python
# GET /s/<code>/
# Redirects to original URL
```

## Configuration

```python
# settings.py
SHORT_URL_DOMAIN = 'short.example.com'
SHORT_URL_ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
```
