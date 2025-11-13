# Third-Party Integrations

Ready-to-use connectors for 45+ external services and APIs.

## Overview

The `lib` module provides integration adapters for:

- **Cloud Services** - AWS, Google Cloud, Azure
- **Payment & Billing** - Stripe, Zuora, PayPal
- **Communication** - Slack, Discord, Twilio, Gmail
- **Data & CRM** - Airtable, Salesforce, Hubspot
- **Commerce** - Shopify, Stripe
- **Maps & Location** - Google Maps, Mapbox, Zillow
- **Analytics & Events** - Iterable, Mixpanel
- **Business Services** - Indeed, ZipRecruiter, Yelp

## Payment & Billing

### Stripe
Full Stripe integration for payments, subscriptions, and invoicing:

```python
from htk.lib.stripe_lib.models import BaseStripeCustomer
from htk.lib.stripe_lib.utils import charge_card

# Create customer
customer = charge_card(user, amount, stripe_token)

# Handle subscriptions
subscription = customer.create_subscription(plan_id)
customer.change_subscription_plan(subscription_id, new_plan)
```

**Classes:** `BaseStripeCustomer`, `BaseStripeSubscription`, `BaseStripePlan`

### Zuora
Subscription and billing management:

```python
from htk.lib.zuora.api import get_subscription, update_subscription

subscription = get_subscription(subscription_id)
update_subscription(subscription_id, new_params)
```

## Communication

### Slack
Send messages, handle webhooks, and integrate with Slack:

```python
from htk.lib.slack.utils import webhook_call

webhook_call({'text': 'Hello from HTK!', 'channel': '#notifications'})
```

**Features:**
- Webhook event handling
- Message posting
- Event handlers for various Slack events
- Beacon/location tracking

### Discord
Discord webhook integration:

```python
from htk.lib.discord.views import discord_webhook_relay_view
```

### Gmail
Interact with Gmail API:

```python
from htk.lib.google.gmail.api import GmailAPI

gmail = GmailAPI()
messages = gmail.messages_list()
```

### Twilio / Plivo
SMS and messaging:

```python
from htk.lib.plivo.utils import handle_message_event
```

## Cloud Storage

### AWS S3
Store and retrieve files from S3:

```python
from htk.lib.aws.s3.utils import S3Manager

s3 = S3Manager()
s3.put_file('bucket', 'key', file_obj)
s3.get_url('bucket', 'key')
```

**Classes:** `S3Manager`, `S3MediaAsset`

### Google Cloud
Cloud services via Google APIs:

```python
from htk.lib.google.sheets.api import spreadsheets_values_append
from htk.lib.google.translate.utils import translate

translate('Hello', 'en', 'es')
```

## Maps & Location

### Google Maps
Google Maps API utilities:

```python
from htk.lib.google.maps.utils import get_map_url_for_geolocation
from htk.lib.google.geocode.api import geocode

map_url = get_map_url_for_geolocation(latitude, longitude)
```

### Mapbox
Mapbox geolocation and mapping:

```python
from htk.lib.mapbox.geocode import reverse_geocode

address = reverse_geocode(latitude, longitude)
```

### Zillow / Redfin
Real estate data:

```python
from htk.lib.zillow.utils import get_zestimate
from htk.lib.redfin.api import get_avm

zestimate = get_zestimate(zpid)
avm = get_avm(property_id)
```

## E-commerce & Payments

### Shopify
Shopify API integration:

```python
from htk.lib.shopify_lib.api import iter_products, iter_orders

for product in iter_products():
    print(product.name)
```

**Classes:** `ShopifyProduct`, `ShopifyOrder`, `ShopifyCustomer`

### Airtable
Airtable API for spreadsheet-like data:

```python
from htk.lib.airtable.api import AirtableAPI

api = AirtableAPI()
records = api.fetch_records('table_name')
```

## Data & CRM

### Full Contact
Person lookup and data enrichment:

```python
from htk.lib.fullcontact.utils import find_person_by_email

person = find_person_by_email('user@example.com')
```

### Indeed
Job posting and applicant tracking:

```python
from htk.lib.indeed.api.job_sync import IndeedJobSyncAPI

api = IndeedJobSyncAPI()
api.create_job(job_data)
```

### ZipRecruiter
Job posting platform:

```python
from htk.lib.ziprecruiter.api import ZipRecruiterAPI

api = ZipRecruiterAPI()
```

## Analytics & Events

### Iterable
Email and SMS marketing automation:

```python
from htk.lib.iterable.utils import get_iterable_api_client

client = get_iterable_api_client()
client.track_event(user_id, event_name, data)
```

## Search & Enrichment

### Yelp
Business search and reviews:

```python
from htk.lib.yelp.api import business_lookup

business = business_lookup('business_name', location)
```

### GitHub
GitHub API integration:

```python
from htk.lib.github.utils import get_repository, sync_repository_releases

repo = get_repository('owner/repo')
sync_repository_releases(repo)
```

## Utilities & Helpers

### QR Codes
Generate QR codes:

```python
from htk.lib.qrcode.utils import qrcode_image_response

return qrcode_image_response('https://example.com')
```

### Weather
Weather data:

```python
from htk.lib.darksky.utils import generate_weather_report
```

### Geolocation
IP-based location lookup:

```python
from htk.lib.geoip.utils import get_country_code_by_ip, get_timezone_by_ip

country = get_country_code_by_ip('8.8.8.8')
```

### OpenAI
Chat completions and AI:

```python
from htk.lib.openai.adapter import chat_completion

response = chat_completion(messages)
```

## Integration Patterns

### Authentication
Most integrations require API keys in settings:

```python
# settings.py
STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY')
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
```

### Error Handling
Use safe wrappers for API calls:

```python
from htk.lib.stripe_lib.utils import safe_stripe_call

try:
    result = safe_stripe_call(lambda: stripe.Charge.create(...))
except Exception as e:
    log.error(f"Stripe error: {e}")
```

## Quick Reference by Use Case

**Need to charge a card?** → Stripe
**Building a marketplace?** → Stripe + Airtable
**Real-time notifications?** → Slack
**Location features?** → Google Maps + Mapbox
**Email marketing?** → Iterable
**Job postings?** → Indeed + ZipRecruiter
**Data enrichment?** → FullContact
**E-commerce?** → Shopify
