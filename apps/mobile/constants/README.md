# Mobile Constants

## Overview

This module defines configuration for mobile app integration, including app store URLs.

## Constants

### App Store Configuration

- **`HTK_APPSTORE_URL`** - Default: `None` - URL to mobile app on app store (iTunes/Google Play)

## Usage Examples

### Configure App Store URLs

```python
# In Django settings.py
HTK_APPSTORE_URL = 'https://apps.apple.com/app/myapp/id123456789'
# For Google Play:
# HTK_APPSTORE_URL = 'https://play.google.com/store/apps/details?id=com.example.myapp'
```

### Get App Store Link in Template

```python
# In Django template
{% load app_config %}
<a href="{{ app_store_url }}" class="btn btn-primary">Download App</a>
```

### Generate App Store Links

```python
# In your view
from django.conf import settings

context = {
    'app_store_url': settings.HTK_APPSTORE_URL,
}
```
