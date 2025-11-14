# Django Apps

Reusable, extensible Django applications for common functionality.

## Overview

HTK provides 29 pre-built apps organized by feature:

- **User Management** - Accounts, profiles, email management
- **Social & Authentication** - OAuth, social auth backends
- **Organization & Teams** - Multi-org support, permissions, invitations
- **Payments & Commerce** - Stripe, subscriptions, quotes, invoices
- **Communication** - Messaging, conversations, notifications
- **Content & Knowledge** - Bible, forums, feedback
- **Data Management** - Files, storage, key-value storage
- **Utilities** - Async tasks, features, changelog, documentation

## User Management

### Accounts (`accounts`)
User registration, authentication, and profile management.

**Key Features:**
- User registration and email verification
- Email management (multiple emails per user)
- Token-based authentication
- User profiles with timezone and locale
- Social auth integration (OAuth, OAuth2)
- Password reset and recovery
- User search and lookup

**Usage:**
```python
from htk.apps.accounts.utils.general import create_user, get_user_by_email

user = create_user('user@example.com', password='secure')
user = get_user_by_email('user@example.com')
```

**Models:**
- `BaseAbstractUserProfile` - Extend for custom user profiles
- `UserEmail` - Multiple emails per user
- Django's built-in `User` model

### Addresses (`addresses`)
Postal address management and geocoding.

**Key Features:**
- Store and manage postal addresses
- Google Maps integration for address geocoding
- Latitude/longitude storage

## Social & Authentication

### OAuth & Social Auth
HTK supports social authentication through `python-social-auth`:
- Facebook, Twitter, Google, LinkedIn
- Withings (health data)
- Custom OAuth2 backends

## Organization & Teams

### Organizations (`organizations`)
Multi-organization support with role-based access control.

**Key Features:**
- Create organizations with members
- Role-based permissions (owner, member, etc.)
- Organization invitations
- Member management
- Organization-specific settings

**Usage:**
```python
from htk.apps.organizations.models import BaseOrganization

org = BaseOrganization.objects.create(name='Acme Corp')
org.invite_member('user@example.com', role='member')
```

### Invitations (`invitations`)
Handle user invitations for onboarding and access control.

**Key Features:**
- Invitation creation and tracking
- Email-based invitations
- Invitation expiration
- Integration with user onboarding

## Payments & Commerce

### Stripe Integration (`stripe_lib`)
Full Stripe integration for payments and subscriptions.

**Key Features:**
- Stripe customer creation and management
- Credit card handling
- One-time charges and payments
- Recurring subscriptions
- Invoice generation

**Usage:**
```python
from htk.apps.stripe_lib.models import BaseStripeCustomer

customer = BaseStripeCustomer.objects.create(user=user, stripe_id='cus_xxx')
customer.charge(amount, stripe_token)
subscription = customer.create_subscription(plan_id)
```

### CPQ (Configure, Price, Quote) (`cpq`)
Quoting and invoicing system.

**Key Features:**
- Create quotes for customers
- Line items and pricing
- Group quotes
- Invoice generation
- Payment tracking

### Customers (`customers`)
Customer management for commerce apps.

### Store (`store`)
E-commerce and store functionality.

## Communication & Notifications

### Notifications (`notifications`)
Send notifications via multiple channels.

**Key Features:**
- Email notifications
- Slack integration
- Notification history and tracking

### Conversations (`conversations`)
User-to-user messaging and conversations.

**Key Features:**
- Create conversations between users
- Message threads with participants
- Emoji reactions to messages
- Conversation history

**Usage:**
```python
from htk.apps.conversations.models import BaseConversation

convo = BaseConversation.objects.create()
convo.add_participants(user1, user2)
convo.add_message(user1, 'Hello!')
```

### Forums (`forums`)
Discussion forums and message threads.

**Key Features:**
- Create forums
- Forum threads and messages
- Tags for categorization
- Thread tracking

## Content & Knowledge

### Bible (`bible`)
Scripture data and reference tools.

**Key Features:**
- Bible books, chapters, verses
- Scripture passage lookup
- Bible reference formatting

### Feedback (`feedback`)
Collect user feedback and reviews.

## Data & File Management

### File Storage (`file_storage`)
Store uploaded files.

**Key Features:**
- Handle file uploads
- Store files securely
- File organization

### Blob Storage (`blob_storage`)
Binary large object (BLOB) storage.

### KV Storage (`kv_storage`)
Key-value storage for flexible data.

**Usage:**
```python
from htk.apps.kv_storage.utils import kv_put, kv_get

kv_put('user:settings', {'theme': 'dark'})
settings = kv_get('user:settings')
```

## Features & Configuration

### Features (`features`)
Feature flags for gradual rollouts.

**Key Features:**
- Enable/disable features per user or org
- A/B testing support
- Feature flag caching

**Usage:**
```python
from htk.apps.features.utils import get_feature_flag

if get_feature_flag('new_dashboard', user):
    # Show new dashboard
```

### Maintenance Mode (`maintenance_mode`)
Enable maintenance mode to prevent user access.

**Key Features:**
- Global maintenance mode toggle
- Exception list for admin access

### Prelaunch (`prelaunch`)
Pre-launch signup and early access management.

## API & Documentation

### API (`api`)
REST API utilities and tools. See [api/README.md](../api/README.md).

### Documentation (`documentation`)
Automatic README generation for modules.

**Key Features:**
- Analyze Python modules
- Generate documentation
- Extract classes, functions, models

### Changelog (`changelog`)
Track and generate changelogs from Git history.

## Localization & Internationalization

### i18n (`i18n`)
Internationalization and localization tools.

**Key Features:**
- Multi-language string support
- Localizable and localized strings
- Language detection

### Sites (`sites`)
Multi-site support (Django contrib wrapper).

## Miscellaneous

### Mobile (`mobile`)
Mobile app integration and push notifications.

### MP (Materialized Properties) (`mp`)
Performance optimization through materialized properties.

### Tokens (`tokens`)
API token management and authentication.

### URL Shortener (`url_shortener`)
Create and manage short URLs.

**Usage:**
```python
from htk.apps.url_shortener.models import HTKShortUrl

short = HTKShortUrl.objects.create(url='https://very-long-url.com')
short_code = short.code  # e.g., 'a7f2'
```

## Development Patterns

### Extending Apps

Extend abstract models to add custom fields:

```python
from htk.apps.accounts.models import BaseAbstractUserProfile

class CustomUserProfile(BaseAbstractUserProfile):
    organization = ForeignKey(Organization)
    department = CharField(max_length=100)
```

### Using Mixins

Leverage app mixins for common functionality:

```python
from htk.apps.accounts.mixins import UserOwnedMixin

class MyModel(UserOwnedMixin):
    # Automatically tracks owner and timestamps
    pass
```

### Signal Handlers

Apps provide signal handlers for key events:

```python
from htk.apps.accounts.apps import create_user_profile

# Automatically called when User is created
```

## Installation

Enable apps in `settings.py`:

```python
INSTALLED_APPS = [
    'htk.apps.accounts',
    'htk.apps.organizations',
    'htk.apps.stripe_lib',
    'htk.apps.conversations',
    'htk.apps.notifications',
    # ... more apps
]
```

Each app includes migrations for easy database setup:

```bash
python manage.py migrate
```
