# Maintenance Mode Constants

## Overview

This module defines configuration for activating and managing maintenance mode, including the toggle setting and the associated view URL.

## Constants

### Maintenance Configuration

- **`HTK_MAINTENANCE_MODE`** - Default: `False` - Enable maintenance mode (blocks regular users)
- **`HTK_MAINTENANCE_MODE_URL_NAME`** - Default: `'maintenance_mode'` - URL name for maintenance mode view

## Usage Examples

### Activate Maintenance Mode

```python
# In Django settings.py
HTK_MAINTENANCE_MODE = True
HTK_MAINTENANCE_MODE_URL_NAME = 'maintenance_mode'
```

### Check in Middleware

```python
from django.conf import settings
from htk.apps.maintenance_mode.constants import HTK_MAINTENANCE_MODE

if settings.HTK_MAINTENANCE_MODE:
    # Redirect user to maintenance mode page
    pass
```

### Get Maintenance View URL

```python
from django.urls import reverse
from django.conf import settings

if settings.HTK_MAINTENANCE_MODE:
    maintenance_url = reverse(settings.HTK_MAINTENANCE_MODE_URL_NAME)
```
