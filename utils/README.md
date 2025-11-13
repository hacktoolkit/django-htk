# Utilities

Common helper functions and utilities for everyday tasks.

## Overview

The `utils` module provides practical utilities organized by purpose:

- **Text Processing** - Formatting, sanitization, translation, transformations
- **Caching** - Memoization and cached attributes
- **Data Structures** - Dictionaries, enums, collections
- **DateTime** - Timezone handling, conversions, scheduling
- **HTTP/Requests** - Response handling, CORS, caching headers
- **JSON** - Path traversal, value extraction
- **Database** - Raw SQL, migrations, connection management
- **Email** - Parsing, enrichment, permutations
- **Handles** - Unique identifiers and slugs
- **Images** - Format detection, processing
- **Payments** - Luhn validation, card handling
- **PDF/CSV** - File generation and export
- **Queries** - Bulk operations, object retrieval
- **Security** - Encryption, HTTPS detection

## Text Processing

### Formatting & Display

```python
from htk.utils.text.pretty import phonenumber
from htk.utils.text.english import pluralize_noun, oxford_comma

phone = phonenumber('5551234567')
message = oxford_comma(['Alice', 'Bob', 'Charlie'])  # Alice, Bob, and Charlie
items_text = pluralize_noun('item', count)  # 'items' or 'item'
```

### Conversion

```python
from htk.utils.text.converters import html2markdown, markdown2slack

markdown = html2markdown('<b>Bold</b> text')
slack_msg = markdown2slack('**Bold** text')
```

### Transformations

```python
from htk.utils.text.transformers import ellipsize, seo_tokenize
from htk.utils.text.transformers import snake_case_to_camel_case

text = ellipsize('Very long text', max_len=20)  # 'Very long ...'
tokens = seo_tokenize('my-product-name')
camel = snake_case_to_camel_case('user_id')  # 'userId'
```

### Sanitization & Unicode

```python
from htk.utils.text.unicode import demojize, unicode_to_ascii

clean = demojize('Hello 👋')  # 'Hello'
ascii_text = unicode_to_ascii('Café')  # 'Cafe'
```

## Caching & Optimization

### Decorators

```python
from htk.utils.cache_descriptors import memoized, CachedAttribute

@memoized
def expensive_function(x):
    return x ** 2

class MyClass:
    @CachedAttribute
    def computed_value(self):
        return sum(range(1000))  # Computed once, cached forever
```

### Memoization

```python
from htk.utils.cache_descriptors import CachedClassAttribute

class Config:
    @CachedClassAttribute
    def settings(cls):
        return load_settings()
```

## Data Structures

### Dictionaries

```python
from htk.utils.data_structures.general import filter_dict

filtered = filter_dict({'a': 1, 'b': 2, 'c': 3}, ['a', 'c'])  # {'a': 1, 'c': 3}
```

### Enums

```python
from htk.utils.enums import enum_to_str, choices

class Status(Enum):
    ACTIVE = 1
    INACTIVE = 2

status_str = enum_to_str(Status.ACTIVE)
status_choices = choices(Status)  # [(1, 'ACTIVE'), (2, 'INACTIVE')]
```

### Collections

```python
from htk.utils.iter_utils import chunks, lookahead

for group in chunks(items, 10):
    process_batch(group)  # Process 10 items at a time
```

## DateTime & Timezone

### Timezone Handling

```python
from htk.utils.datetime_utils import localized_datetime
from htk.utils.datetime_utils import is_within_hour_bounds_for_timezone

dt = localized_datetime(naive_dt, 'America/New_York')
is_business_hours = is_within_hour_bounds_for_timezone('America/New_York', 9, 17)
```

### Conversions

```python
from htk.utils.datetime_utils import datetime_to_unix_time, iso_to_gregorian

timestamp = datetime_to_unix_time(datetime.now())
gregorian_date = iso_to_gregorian(2024, 1, 1)  # ISO week to Gregorian
```

## HTTP & Requests

### Response Headers

```python
from htk.utils.http.response import set_cache_headers, set_cors_headers_for_image

response = set_cache_headers(response, max_age=3600)  # Cache for 1 hour
response = set_cors_headers_for_image(response)
```

### Request Parsing

```python
from htk.utils.request import extract_request_param, parse_authorization_header

user_id = extract_request_param(request, 'user_id', int)
auth_type, token = parse_authorization_header(request)
```

## JSON & Data

### JSON Path Traversal

```python
from htk.utils.json_utils import find_json_value, find_all_json_paths

value = find_json_value(data, 'user.profile.name')  # Dot notation
paths = find_all_json_paths(data)  # All valid paths
```

### Compression

```python
from htk.utils.json_utils import deepcopy_with_compact

clean_data = deepcopy_with_compact(data)  # Removes None values
```

## Email & Contact

### Email Utilities

```python
from htk.utils.emails import email_permutator, find_company_emails_for_name

# Generate email variations for John Smith at acme.com
emails = email_permutator('acme.com', 'John', 'Smith')
# ['john.smith@acme.com', 'jsmith@acme.com', 'john@acme.com', ...]
```

## Handles & Identifiers

### Unique Handles

```python
from htk.utils.handles import generate_unique_handle, is_unique_handle

handle = generate_unique_handle('John Smith')  # 'john-smith', 'john-smith-2', etc.
```

## Images

### Format Detection

```python
from htk.utils.image import detect_image_format

format = detect_image_format(image_file)  # 'PNG', 'JPEG', etc.
```

## Validation

### Payment Cards

```python
from htk.utils.luhn import is_luhn_valid, calculate_luhn_check_digit

valid = is_luhn_valid('4532015112830366')
check_digit = calculate_luhn_check_digit('453201511283036')
```

## Database

### Raw SQL

```python
from htk.utils.db import raw_sql, namedtuplefetchall

results = raw_sql('SELECT * FROM users WHERE active = %s', [True])
rows = namedtuplefetchall(cursor)  # Returns named tuples
```

### Connection Management

```python
from htk.utils.db import ensure_mysql_connection_usable

ensure_mysql_connection_usable()  # Reconnect if needed
```

## PDF & CSV

### CSV Export

```python
from htk.utils.csv_utils import get_csv_response

response = get_csv_response(filename, [['Name', 'Email'], ['John', 'john@example.com']])
```

### PDF Generation

```python
from htk.utils.pdf_utils import render_to_pdf_response

response = render_to_pdf_response('template.html', context_data)
```

## Queries & Lookups

### Bulk Operations

```python
from htk.utils.query import get_objects_by_id

users = get_objects_by_id(User, [1, 2, 3])  # In single query
```

### Safe Retrieval

```python
from htk.utils.django_shortcuts import get_object_or_none

user = get_object_or_none(User, id=999)  # Returns None instead of exception
```

## Security

### Encryption

```python
from htk.utils.crypto import AESCipher

cipher = AESCipher()
encrypted = cipher.encrypt('sensitive data')
decrypted = cipher.decrypt(encrypted)
```

### HTTPS Detection

```python
from htk.utils.security import should_use_https

if should_use_https():
    url = f'https://{host}/path'
```

## Terminal Output

### ANSI Colors

```python
from htk.utils.xterm import colorize, c

colored_text = colorize('Error!', fg='red', style='bold')
msg = c('Success!', 'green')  # Shorthand
```

## Common Patterns

**Processing CSV with Django models:**
```python
from htk.utils.csv_utils import UnicodeReader

with open('data.csv') as f:
    for row in UnicodeReader(f):
        User.objects.create(email=row[0], name=row[1])
```

**Paginating large datasets:**
```python
from htk.utils.iter_utils import chunks

for batch in chunks(User.objects.all(), 100):
    process_users(batch)
```

**Building URLs with parameters:**
```python
from htk.utils.urls import build_url_with_query_params

url = build_url_with_query_params('/search/', {'q': 'django', 'page': 2})
```
