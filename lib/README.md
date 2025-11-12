# HTK Lib Module

> 47+ integrations with external services: Cloud, payments, messaging, social, data, and more.

## Purpose

The lib module provides modular integrations with external services and APIs. Use only the integrations you need—optional dependencies keep your project lightweight.

## Integrations by Category

| Category | Services |
|----------|----------|
| **Cloud** (6) | AWS (S3, EC2, Lambda, CloudFront, SNS/SQS), Google Cloud, Mapbox, MongoDB, RabbitMQ |
| **Messaging** (7) | Slack, Discord, Mailchimp, Iterable, Plivo (SMS/Voice), OpenAI, Alexa |
| **Social** (6) | Google OAuth, Facebook, Twitter, LinkedIn, GitHub, Apple Sign In |
| **Payments** (3) | Stripe, Zuora, payment processing |
| **Data** (4) | Airtable, FullContact, DarkSky, GeoIP |
| **Real Estate** (4) | Zillow, Redfin, Yelp, Indeed, ZipRecruiter, Glassdoor |
| **Food & Lifestyle** (3) | OhMyGreen, Yelp, Zesty CMS |
| **Other** (6) | Bible APIs (ESV, LiteralWord, AwesomeBible), QR Codes, Gravatar, Shopify, SongSelect |

## Quick Start

```python
from htk.lib.slack.utils import send_slack_message
from htk.lib.stripe_lib.utils import process_payment

# Send Slack notification
send_slack_message(channel='#general', message='Hello from HTK')

# Process payment
result = process_payment(amount=9999, token='tok_visa')
```

## Common Integration Patterns

### Slack Notifications

```python
from htk.lib.slack.utils import send_slack_message

send_slack_message(
    channel='#alerts',
    message='Order #123 processed',
    icon_emoji=':package:'
)
```

### Payment Processing (Stripe)

```python
from htk.lib.stripe_lib.utils import process_payment, create_subscription

# Process one-time payment
result = process_payment(
    amount=9999,  # cents
    currency='usd',
    token='tok_visa'
)

# Create subscription
subscription = create_subscription(customer_id, plan='premium')
```

### Email Marketing (Mailchimp)

```python
from htk.lib.mailchimp.utils import add_subscriber, send_campaign

add_subscriber(list_id, email, name='John')
send_campaign(campaign_id)
```

### Geocoding (Google Maps)

```python
from htk.lib.google.geocode.utils import geocode_address

location = geocode_address('123 Main St, New York, NY')
# Returns: {'lat': 40.7128, 'lng': -74.0060}
```

### User Enrichment (FullContact)

```python
from htk.lib.fullcontact.utils import enrich_user
from htk.lib.gravatar.utils import get_gravatar

avatar = get_gravatar(email)
profile = enrich_user(email)
```

## Configuration

Each integration requires setup in `settings.py`:

```python
# Slack
HTK_SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
HTK_SLACK_NOTIFICATIONS_ENABLED = True

# Stripe
HTK_STRIPE_API_KEY = 'sk_live_...'
HTK_STRIPE_PUBLIC_KEY = 'pk_live_...'

# Google Maps
HTK_GOOGLE_MAPS_API_KEY = 'your_api_key'
HTK_GOOGLE_MAPS_ENABLED = True

# OAuth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'your-key'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'your-secret'
```

## Cloud & Infrastructure

**AWS** - S3, EC2, Lambda, CloudFront, SNS/SQS
```python
from htk.lib.aws.s3.utils import upload_to_s3, download_from_s3

upload_to_s3(file_obj, bucket, key)
data = download_from_s3(bucket, key)
```

**Google Services** (9 sub-modules: Maps, Sheets, Gmail, YouTube, reCAPTCHA, Cloud Messaging, Translate, Chat)
```python
from htk.lib.google.maps.utils import get_directions
directions = get_directions(origin, destination)
```

**MongoDB** - Document storage and aggregation
```python
from htk.lib.mongodb.utils import connect, query

client = connect()
results = client[db][collection].find({})
```

## Communication & Messaging

**Slack** - Channel messages, webhooks, bot integration
```python
from htk.lib.slack.utils import send_slack_message, post_to_channel

send_slack_message(channel, message)
post_to_channel(channel_id, text)
```

**Plivo** - SMS and voice calls
```python
from htk.lib.plivo.utils import send_sms, make_call

send_sms(to_number, message)
make_call(to_number, from_number)
```

**OpenAI** - ChatGPT and text completion
```python
from htk.lib.openai.utils import complete_text, chat_completion

response = complete_text(prompt)
chat_reply = chat_completion(messages)
```

## Social & Authentication

**OAuth Providers** - Google, Facebook, Twitter, LinkedIn, GitHub, Apple
```python
# OAuth is integrated with htk.apps.accounts
# See accounts app README for configuration
```

## Payments

**Stripe** - Payment processing and subscriptions
```python
from htk.lib.stripe_lib.utils import (
    process_payment,
    create_subscription,
    refund_charge,
)

process_payment(amount, token)
subscription = create_subscription(customer, plan)
refund_charge(charge_id)
```

## Best Practices

- **Conditional imports** - Wrap in try/except to handle missing dependencies
- **Configuration validation** - Check settings before using integration
- **Error handling** - Don't fail main operation if integration fails
- **Rate limiting** - Cache results and respect API rate limits
- **Logging** - Log integration calls for debugging
- **Security** - Never commit API keys; use environment variables

### Error Handling Example

```python
try:
    send_slack_message(channel, message)
except Exception as e:
    logger.exception('Slack notification failed')
    # Don't fail the main operation
```

### Conditional Import Example

```python
try:
    from htk.lib.stripe_lib.utils import process_payment
    STRIPE_ENABLED = True
except ImportError:
    STRIPE_ENABLED = False

if not STRIPE_ENABLED:
    raise ImproperlyConfigured('Stripe not configured')
```

## Adding New Integrations

1. Create module directory: `mkdir -p htk/lib/myservice`
2. Implement utils: `htk/lib/myservice/utils.py`
3. Add constants if needed: `htk/lib/myservice/constants/__init__.py`
4. Write tests and document in README

Example:
```python
# htk/lib/myservice/utils.py
from django.conf import settings

def call_service(**kwargs):
    api_key = getattr(settings, 'HTK_MYSERVICE_API_KEY', None)
    if not api_key:
        raise ImproperlyConfigured('HTK_MYSERVICE_API_KEY not set')
    # API call implementation
```

## Related Modules

- `htk.apps.accounts` - OAuth and social authentication
- `htk.apps.notifications` - Notification delivery
- `htk.api` - REST API utilities
- `htk.utils` - General utility functions

## References

- Individual service API documentation
- HTK source code examples
- [OAuth 2.0 Security Best Practices](https://tools.ietf.org/html/draft-ietf-oauth-security-topics)

## Status & Maintenance

**Actively Maintained**: Google, Stripe, Slack, AWS, OpenAI

**Community Maintained**: GitHub, Discord, Twitter, real estate APIs

**Potentially Outdated**: Check specific integration documentation

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
- **Dependencies:** Most integrations are optional; install as needed
