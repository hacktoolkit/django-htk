# Mobile App

Mobile device detection, registration, and push notifications.

## Quick Start

```python
from htk.apps.mobile.models import MobileDevice
from htk.apps.mobile.utils import is_mobile_request

# Check if request from mobile
if is_mobile_request(request):
    template = 'mobile_view.html'
else:
    template = 'desktop_view.html'

# Register device
device = MobileDevice.objects.create(
    user=user,
    device_id='device_123_abc',
    platform='ios',  # 'ios' or 'android'
    version='17.0',
    device_name='iPhone 15'
)

# Track active devices
active_count = user.mobiledevice_set.filter(is_active=True).count()
```

## Mobile Device Management

### Register Devices

```python
from htk.apps.mobile.models import MobileDevice

# Create device with push token
device = MobileDevice.objects.create(
    user=user,
    device_id='uuid-123',
    platform='android',
    version='14',
    push_token='firebase_token_123',
    device_name='Samsung Galaxy S24'
)

# Or update existing device
device, created = MobileDevice.objects.update_or_create(
    user=user,
    device_id='uuid-123',
    defaults={
        'push_token': 'new_firebase_token',
        'is_active': True
    }
)
```

### Detect Mobile Requests

```python
from htk.apps.mobile.utils import is_mobile_request

def my_view(request):
    if is_mobile_request(request):
        # Return mobile optimized response
        return JsonResponse({'mobile': True})
    else:
        # Return desktop response
        return JsonResponse({'mobile': False})
```

### Send Push Notifications

```python
from htk.apps.mobile.models import MobileDevice

# Get user's devices
devices = MobileDevice.objects.filter(user=user, is_active=True)

# Send push to all devices
for device in devices:
    device.send_push_notification(
        title='New Message',
        message='You have a new message from John',
        data={'message_id': 123, 'sender_id': 456}
    )
```

## Common Patterns

### Multi-Device Support

```python
from htk.apps.mobile.models import MobileDevice

# Get all active devices for user
active_devices = MobileDevice.objects.filter(
    user=user,
    is_active=True
)

# Send notification to all devices
message = 'Important update available'
for device in active_devices:
    device.send_push_notification(
        title='Update',
        message=message
    )

# Track device count
device_count = active_devices.count()
```

### Device Deactivation

```python
from htk.apps.mobile.models import MobileDevice

# Deactivate old devices
devices_to_remove = MobileDevice.objects.filter(
    user=user,
    last_seen__lt=timezone.now() - timedelta(days=90)
)

for device in devices_to_remove:
    device.is_active = False
    device.save()
```

### Platform-Specific Logic

```python
from htk.apps.mobile.models import MobileDevice

# Send different notifications by platform
ios_devices = MobileDevice.objects.filter(user=user, platform='ios')
android_devices = MobileDevice.objects.filter(user=user, platform='android')

# iOS specific
for device in ios_devices:
    device.send_push_notification(
        title='iOS Notification',
        message='This is iOS specific',
        sound='default',
        badge=1
    )

# Android specific
for device in android_devices:
    device.send_push_notification(
        title='Android Notification',
        message='This is Android specific',
        priority='high',
        color='#FF5722'
    )
```

### Track Device Usage

```python
from django.utils import timezone
from htk.apps.mobile.models import MobileDevice

# Update last seen
device = MobileDevice.objects.get(device_id=device_id)
device.last_seen = timezone.now()
device.save()

# Get most recently active devices
recent = MobileDevice.objects.filter(user=user).order_by('-last_seen')[:5]

# Identify inactive devices
inactive_cutoff = timezone.now() - timedelta(days=30)
inactive = MobileDevice.objects.filter(
    user=user,
    last_seen__lt=inactive_cutoff
)
```

## Models

### MobileDevice

Track user's mobile devices:

```python
class MobileDevice(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    device_id = CharField(max_length=200, unique=True)  # UUID
    platform = CharField(max_length=20)  # 'ios' or 'android'
    version = CharField(max_length=50)
    push_token = CharField(max_length=500, blank=True)
    device_name = CharField(max_length=200, blank=True)
    is_active = BooleanField(default=True)
    last_seen = DateTimeField(auto_now=True)
    created = DateTimeField(auto_now_add=True)
```

## Configuration

```python
# settings.py
MOBILE_PUSH_PROVIDER = 'firebase'  # or 'apns' for iOS

# Firebase configuration
FIREBASE_CREDENTIALS = os.environ.get('FIREBASE_CREDENTIALS')
FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID')

# Apple Push Notification Service (APNS)
APNS_CERTIFICATE_PATH = os.environ.get('APNS_CERTIFICATE_PATH')
APNS_KEY_PATH = os.environ.get('APNS_KEY_PATH')

# Device tracking
MOBILE_DEVICE_RETENTION_DAYS = 180  # Keep inactive devices for 6 months
```

## Best Practices

1. **Store push tokens securely** - Encrypt push tokens in database
2. **Handle device deactivation** - Clean up when user logs out
3. **Respect notification preferences** - Check user settings before sending
4. **Handle push errors** - Remove devices with invalid tokens
5. **Platform-specific features** - Send appropriate payloads per platform
6. **Track device identifiers** - Prevent duplicate registrations
7. **Test before production** - Use development certificates for testing

## Related Modules

- `htk.apps.accounts` - User management
- `htk.apps.notifications` - Notification system
- `htk.middleware` - User agent detection
