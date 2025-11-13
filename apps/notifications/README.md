# Notifications App

Send notifications across multiple channels (email, SMS, in-app).

## Quick Start

```python
from htk.apps.notifications.utils import notify

# Send notification
notify(
    user=user,
    message='Order shipped!',
    channel='email',
    subject='Your order is on the way'
)

# Send to multiple users
notify_users = [user1, user2, user3]
for u in notify_users:
    notify(u, 'New feature available', channel='email')
```

## Channels

- **Email** - Django email backend
- **SMS** - Twilio/Plivo integration
- **In-app** - Store in database, display in UI
- **Slack** - Send to Slack

## Common Patterns

```python
# Email notification
notify(user, 'Welcome!', channel='email', subject='Welcome to MyApp')

# In-app notification (persistent)
notify(user, 'You have a new message', channel='in_app')

# Multi-channel
for channel in ['email', 'in_app']:
    notify(user, message, channel=channel)
```

## Integration Examples

```python
# Notify on order creation
from django.db.models.signals import post_save

@receiver(post_save, sender=Order)
def notify_on_order(sender, instance, created, **kwargs):
    if created:
        notify(instance.user, f'Order #{instance.id} created', channel='email')
```

## Related Modules

- `htk.apps.accounts` - User management
- `htk.lib.slack` - Slack integration
