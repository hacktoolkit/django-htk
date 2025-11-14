# Zuora Integration

Billing, subscriptions, and revenue management.

## Quick Start

```python
from htk.lib.zuora.api import get_subscription, update_subscription, cancel_subscription

# Get subscription
subscription = get_subscription(subscription_id)

# Update subscription
updated = update_subscription(subscription_id, {'status': 'Active'})

# Cancel subscription
cancel_subscription(subscription_id)
```

## Operations

```python
from htk.lib.zuora.utils import ZuoraAPI

api = ZuoraAPI()

# Query subscriptions
subs = api.query('select Id, Status from Subscription where AccountId = ?', [account_id])

# Create invoice
invoice = api.create_invoice(account_id, subscription_id)

# Process payment
payment = api.process_payment(account_id, amount)
```

## Configuration

```python
# settings.py
ZUORA_API_ENDPOINT = os.environ.get('ZUORA_API_ENDPOINT')
ZUORA_CLIENT_ID = os.environ.get('ZUORA_CLIENT_ID')
ZUORA_CLIENT_SECRET = os.environ.get('ZUORA_CLIENT_SECRET')
```
