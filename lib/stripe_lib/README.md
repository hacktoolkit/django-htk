# Stripe Integration

Payment processing, subscriptions, and invoice management.

## Quick Start

```python
from htk.apps.stripe_lib.utils import create_customer, charge_card

# Create customer
customer = create_customer(user, stripe_token)

# Charge card (one-time)
charge = charge_card(customer, amount=1000, currency='usd')

# Create subscription
subscription = customer.create_subscription(plan_id='price_xxx')

# Change plan
customer.change_subscription_plan(subscription_id, new_plan='price_yyy')
```

## Models

- **`BaseStripeCustomer`** - Stripe customer linked to user
- **`BaseStripeSubscription`** - Recurring subscription
- **`BaseStripeProduct`** - Product/plan
- **`BaseStripePrice`** - Pricing

## Common Patterns

```python
# List charges
charges = customer.get_charges()

# Create invoice
invoice = customer.create_invoice()

# Add card
customer.add_card(stripe_token)

# Cancel subscription
customer.cancel_subscription(subscription_id)
```

## Webhooks

```python
from htk.lib.stripe_lib.utils import handle_event

# POST /stripe/webhook/
# Automatically handles Stripe events
```

## Configuration

```python
# settings.py
STRIPE_API_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
```

## Forms

```python
from htk.lib.stripe_lib.forms import CreditCardForm
# Render credit card form safely
```

## Related Modules

- `htk.apps.cpq` - Quoting system
- `htk.apps.stripe_lib` - App wrapper
