# Stripe Library Constants

## Overview

This module provides configuration and reference constants for Stripe payment API integration.

## Configuration Settings

```python
from htk.lib.stripe_lib.constants import (
    HTK_STRIPE_LIVE_MODE,
    HTK_STRIPE_EVENT_HANDLERS,
    HTK_STRIPE_LOG_UNHANDLED_EVENTS,
    HTK_STRIPE_LOG_TEST_MODE_EVENTS,
    HTK_STRIPE_EVENT_LOGGER,
    HTK_STRIPE_CUSTOMER_HOLDER_RELATED_NAME
)

# Use production or test Stripe keys
HTK_STRIPE_LIVE_MODE = True

# Maps Stripe event types to handler function paths
HTK_STRIPE_EVENT_HANDLERS = {}

# Log Stripe events that don't have handlers
HTK_STRIPE_LOG_UNHANDLED_EVENTS = True

# Log test mode events in production
HTK_STRIPE_LOG_TEST_MODE_EVENTS = True

# Where to log events ('rollbar', etc.)
HTK_STRIPE_EVENT_LOGGER = 'rollbar'

# Django model relationship name for customer owner
HTK_STRIPE_CUSTOMER_HOLDER_RELATED_NAME = 'customer'
```

## Stripe ID Prefixes

```python
from htk.lib.stripe_lib.constants import (
    STRIPE_ID_PREFIX_CARD,
    STRIPE_ID_PREFIX_CHARGE,
    STRIPE_ID_PREFIX_CUSTOMER,
    STRIPE_ID_PREFIX_TOKEN
)

# Stripe object ID prefixes
STRIPE_ID_PREFIX_CARD = 'card_'
STRIPE_ID_PREFIX_CHARGE = 'ch_'
STRIPE_ID_PREFIX_CUSTOMER = 'cus_'
STRIPE_ID_PREFIX_TOKEN = 'tok_'
```

## Test Cards

```python
from htk.lib.stripe_lib.constants import STRIPE_TEST_CARDS, DEFAULT_STRIPE_CURRENCY

# Test card numbers for different card types
test_cards = STRIPE_TEST_CARDS
# {
#     'visa': '4242424242424242',
#     'visa_debit': '4000056655665556',
#     'mc': '5555555555554444',
#     'amex': '378282246310005',
#     ...
# }

# Default currency for Stripe charges
DEFAULT_STRIPE_CURRENCY = 'usd'
```

## Usage

```python
from htk.lib.stripe_lib.constants import STRIPE_TEST_CARDS, DEFAULT_STRIPE_CURRENCY

# Use test card in development
test_card = STRIPE_TEST_CARDS.get('visa')

# Create charge with default currency
charge_amount_cents = 9999  # $99.99
```

## Customization

Override settings in `settings.py`:

```python
HTK_STRIPE_LIVE_MODE = False  # Use test mode
HTK_STRIPE_EVENT_HANDLERS = {
    'charge.succeeded': 'myapp.handlers.handle_charge_succeeded',
    'charge.failed': 'myapp.handlers.handle_charge_failed',
}
```
