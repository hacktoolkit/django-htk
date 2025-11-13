# Mobile App

Mobile device detection and mobile-specific features.

## Quick Start

```python
from htk.apps.mobile.models import MobileDevice

# Register device
device = MobileDevice.objects.create(
    user=user,
    device_id='device_123',
    platform='ios',
    version='17.0'
)

# Track active devices
user.mobiledevice_set.filter(is_active=True).count()
```

## Common Patterns

```python
# Detect if request from mobile
from htk.apps.mobile.utils import is_mobile_request
if is_mobile_request(request):
    return render(request, 'mobile.html')

# Send push notification
device.send_push_notification('New message!')
```

## Models

- **`MobileDevice`** - Track user devices

## Related Modules

- `htk.apps.accounts` - User management
- `htk.apps.notifications` - Push notifications
