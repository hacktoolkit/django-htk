# Iterable Integration

Email and SMS marketing automation.

## Quick Start

```python
from htk.lib.iterable.utils import get_iterable_api_client

client = get_iterable_api_client()

# Track event
client.track_event(user_id, 'purchase', {'amount': 100})

# Notify sign up
client.notify_sign_up(user)

# Trigger workflow
client.trigger_workflow(user_id, workflow_id)

# Update email
client.update_user_email(user_id, new_email)
```

## Common Operations

```python
# Get campaign/list/workflow IDs
campaign_id = get_campaign_id('welcome_series')
list_id = get_list_id('active_users')
workflow_id = get_workflow_id('onboarding')

# Get person data
person = client.get_person(email='user@example.com')

# Get batch of people
people = client.get_persons(['user1@example.com', 'user2@example.com'])
```

## Configuration

```python
# settings.py
ITERABLE_API_KEY = os.environ.get('ITERABLE_API_KEY')
```

## Related Modules

- `htk.apps.notifications` - Notification system
