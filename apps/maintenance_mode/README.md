# Maintenance Mode App

Global maintenance mode for controlled downtime.

## Overview

The `maintenance_mode` app provides:

- Toggle maintenance mode on/off globally
- Exception list for admin access during maintenance
- Customizable maintenance page
- Middleware integration

## Quick Start

### Enable Maintenance Mode

```python
from htk.apps.maintenance_mode.utils import enable_maintenance_mode, disable_maintenance_mode

# Enable
enable_maintenance_mode()

# Disable
disable_maintenance_mode()

# Check status
from htk.apps.maintenance_mode.utils import is_maintenance_mode
if is_maintenance_mode():
    # Do something
    pass
```

### Add Exception Users

```python
from django.contrib.auth.models import User

# Users who can access during maintenance
admin_user = User.objects.get(username='admin')
add_maintenance_exception(admin_user)

# Remove exception
remove_maintenance_exception(admin_user)
```

## Installation

```python
# settings.py
MIDDLEWARE = [
    'htk.apps.maintenance_mode.middleware.MaintenanceModeMiddleware',
    # ...
]

# Customize maintenance page template
MAINTENANCE_MODE_TEMPLATE = 'maintenance.html'
MAINTENANCE_MODE_STATUS_CODE = 503  # Service Unavailable
```

## Configuration

```python
# settings.py
HTK_MAINTENANCE_MODE = False  # Set via env or dynamically
MAINTENANCE_MODE_IGNORE_PATHS = [
    '/health/',
    '/status/',
]
MAINTENANCE_MODE_IGNORE_ADMIN = True  # Auto-allow superusers
```

## Common Patterns

### Database Maintenance

```python
# Before starting maintenance
enable_maintenance_mode()

# Run migrations, backups, etc.
# ...

# When complete
disable_maintenance_mode()
```

### Scheduled Maintenance

```python
import schedule
from htk.apps.maintenance_mode.utils import enable_maintenance_mode, disable_maintenance_mode

def maintenance_window():
    enable_maintenance_mode()
    # Do maintenance work
    disable_maintenance_mode()

# Schedule for specific time
schedule.every().day.at('02:00').do(maintenance_window)
```

### Custom Maintenance Page

```html
<!-- templates/maintenance.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Maintenance</title>
</head>
<body>
    <h1>We're undergoing maintenance</h1>
    <p>We'll be back online shortly. Thank you for your patience.</p>
    <p>Expected completion: 02:00 AM EST</p>
</body>
</html>
```

## Views & Templates

```python
# Built-in view
# GET /maintenance/
# Returns 503 Service Unavailable with custom template
```

## Best Practices

1. **Announce in advance** - Tell users when maintenance window is scheduled
2. **Use exceptions sparingly** - Only for support staff if needed
3. **Keep page simple** - Avoid heavy assets during maintenance
4. **Monitor queue** - Don't let requests pile up
5. **Have rollback plan** - Be ready to revert changes
6. **Test before enabling** - Verify maintenance mode works

## API Integration

```python
# API endpoints return 503 with JSON
# GET /api/endpoint/
# Returns: {'error': 'Service under maintenance'}
```
