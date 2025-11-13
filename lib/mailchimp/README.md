# Mailchimp Integration

Email marketing and subscriber management.

## Quick Start

```python
from htk.lib.mailchimp.utils import get_api_url, get_api_data_center

# Determine API endpoint from API key
data_center = get_api_data_center(api_key)
api_url = get_api_url(api_key)
```

## Operations

```python
# Manage lists
api.create_list('Newsletter', contact={'company': 'Acme'})
api.subscribe_to_list(list_id, email)
api.unsubscribe_from_list(list_id, email)

# Send campaigns
api.create_campaign(list_id, campaign_data)
api.send_campaign(campaign_id)
```

## Configuration

```python
# settings.py
MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY')
```

## Related Modules

- `htk.lib.iterable` - Marketing automation
- `htk.apps.notifications` - Email notifications
