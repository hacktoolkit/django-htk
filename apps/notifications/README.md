# Notifications App

Send notifications across multiple channels (email, SMS, in-app, Slack).

## Quick Start

```python
from htk.apps.notifications.utils import notify

# Send email notification
notify(
    user=user,
    message='Order shipped!',
    channel='email',
    subject='Your order is on the way'
)

# Send in-app notification (persistent)
notify(
    user=user,
    message='You have a new message',
    channel='in_app'
)

# Send to multiple users
users = User.objects.filter(organization=org)
for u in users:
    notify(u, 'New feature available', channel='email')
```

## Notification Channels

### Email Channel

Send notifications via Django email backend:

```python
from htk.apps.notifications.utils import notify

notify(
    user=user,
    message='Welcome to our platform!',
    channel='email',
    subject='Welcome',
    html=True  # HTML email
)
```

### SMS Channel

Send SMS via Twilio/Plivo:

```python
from htk.apps.notifications.utils import notify

notify(
    user=user,
    message='Your code is: 123456',
    channel='sms'
)
```

### In-App Channel

Store persistent notifications in database:

```python
from htk.apps.notifications.utils import notify

notify(
    user=user,
    message='You have a new message',
    channel='in_app',
    action_url='/messages/'
)
```

### Slack Channel

Send to Slack:

```python
from htk.apps.notifications.utils import notify

notify(
    user=user,
    message='New order received',
    channel='slack',
    webhook_url='https://hooks.slack.com/services/...'
)
```

## Common Patterns

### Multi-Channel Notifications

```python
from htk.apps.notifications.utils import notify

# Send via multiple channels
channels = ['email', 'in_app']
for channel in channels:
    notify(user, message, channel=channel, subject='Important')
```

### Conditional Notifications

```python
from htk.apps.notifications.utils import notify

# Send based on user preferences
if user.preferences.email_on_order:
    notify(user, 'Order confirmed', channel='email')

if user.preferences.sms_on_urgent:
    notify(user, 'Urgent action needed', channel='sms')
```

### Signal-Based Notifications

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from htk.apps.notifications.utils import notify

@receiver(post_save, sender=Order)
def notify_on_order_creation(sender, instance, created, **kwargs):
    if created:
        notify(
            instance.user,
            f'Order #{instance.order_number} confirmed',
            channel='email',
            subject='Order Confirmation'
        )
```

### Scheduled Notifications

```python
from htk.apps.notifications.utils import notify
from celery import shared_task

@shared_task
def send_reminder_notifications():
    upcoming = Event.objects.filter(
        start_time__gte=timezone.now(),
        start_time__lte=timezone.now() + timedelta(hours=1),
        notified=False
    )

    for event in upcoming:
        notify(
            event.user,
            f'Reminder: {event.name} starts in 1 hour',
            channel='email'
        )
        event.notified = True
        event.save()
```

### Bulk Notifications

```python
from htk.apps.notifications.utils import notify

# Notify multiple users
users = User.objects.filter(
    organization=org,
    is_active=True
)

message = 'Scheduled maintenance tonight 2-4 AM'
for user in users:
    notify(user, message, channel='email')
```

## Notification Models

Access notification history:

```python
from htk.apps.notifications.models import Notification

# Get user's notifications
notifications = Notification.objects.filter(user=user)

# Get unread notifications
unread = notifications.filter(read=False)

# Mark as read
notification.read = True
notification.save()

# Delete old notifications
import datetime
old = Notification.objects.filter(
    created__lt=datetime.datetime.now() - datetime.timedelta(days=30)
)
old.delete()
```

## Configuration

```python
# settings.py
NOTIFICATION_CHANNELS = ['email', 'sms', 'in_app', 'slack']

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# SMS configuration
SMS_PROVIDER = 'twilio'  # or 'plivo'
SMS_ACCOUNT_SID = os.environ.get('SMS_ACCOUNT_SID')
SMS_AUTH_TOKEN = os.environ.get('SMS_AUTH_TOKEN')

# Slack configuration
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')

# In-app notification retention
NOTIFICATION_RETENTION_DAYS = 30
```

## Best Practices

1. **Respect user preferences** - Check notification settings before sending
2. **Use appropriate channels** - Email for important, SMS for urgent, in-app for informational
3. **Avoid notification spam** - Rate limit notifications to same user
4. **Include action URLs** - Help users take action from notifications
5. **Test with staging** - Test notifications in staging before production
6. **Batch process** - Use Celery for bulk notifications
7. **Monitor delivery** - Track sent, failed, bounced notifications

## Related Modules

- `htk.apps.accounts` - User management and preferences
- `htk.lib.slack` - Slack integration
- `htk.lib.plivo` - SMS integration
- `htk.utils.log` - Logging notifications
