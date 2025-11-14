# HTK: Django Hacktoolkit

A comprehensive Django framework providing reusable apps, utilities, and third-party integrations for rapid development. Designed for hackathons and production applications.

## Overview

HTK includes:

- **[Reusable Django Apps](./apps/README.md)** - Pre-built apps for accounts, organizations, payments, messaging, and more
- **[Third-Party Integrations](./lib/README.md)** - Ready-to-use connectors for 45+ external services (Stripe, Google, AWS, Slack, etc.)
- **[Utility Modules](./utils/README.md)** - Common patterns for caching, text processing, APIs, and data handling
- **[API Helpers](./api/README.md)** - Tools for building REST APIs with DataTables support
- **[Form Utilities](./forms/README.md)** - Base form classes and validators
- **[Decorators](./decorators/README.md)** - Django and function decorators for common tasks
- **[Models & Fields](./models/README.md)** - Abstract models and custom Django fields
- **[Middleware](./middleware/README.md)** - Request/response processing utilities

## Quick Start

### Using HTK Apps

HTK provides pre-built Django apps that can be installed and configured in your project:

```python
# settings.py
INSTALLED_APPS = [
    'htk.apps.accounts',
    'htk.apps.organizations',
    'htk.apps.stripe_lib',
    # ... more apps
]
```

### Common Patterns

**Caching objects:**
```python
from htk.cache.classes import CacheableObject

class UserFollowingCache(CacheableObject):
    def get_cache_key_suffix(self):
        return f'user_{self.user_id}_following'
```

**User authentication:**
```python
from htk.apps.accounts.backends import HtkUserTokenAuthBackend
from htk.apps.accounts.utils.auth import login_authenticated_user
```

**API endpoints:**
```python
from htk.api.utils import json_response_form_error, get_object_or_json_error
```

## Key Features

### Accounts & Authentication
- User registration and email verification
- Social authentication backends (OAuth2 support)
- User profiles and email management
- Token-based authentication

### Payments & Billing
- Stripe integration (customers, subscriptions, charges)
- Quote/Invoice system (CPQ)
- Payment tracking and history

### Organizations
- Multi-org support with roles and permissions
- Org invitations and member management
- Permission-based access control

### Messaging & Notifications
- Email notifications
- Slack integration
- Conversation/threading support

### Utilities
- Text processing (formatting, translation, sanitization)
- Caching decorators and schemes
- CSV/PDF generation
- QR codes
- Geolocation and distance calculations
- Timezone handling

### Third-Party Services
See [lib/README.md](./lib/README.md) for details on 45+ integrations including:
- Cloud: AWS S3, Google Cloud
- Communication: Slack, Discord, Gmail, Twilio
- Data: Airtable, Stripe, Shopify, Zuora
- Analytics: Iterable, Mixpanel
- Location: Google Maps, Mapbox, Zillow
- Search: Elasticsearch integration patterns

## Project Structure

```
htk/
├── apps/              # Pre-built Django apps
├── lib/               # Third-party service integrations
├── utils/             # Common utilities and helpers
├── models/            # Abstract models and field types
├── forms/             # Base form classes
├── api/               # REST API utilities
├── decorators/        # Function and class decorators
├── middleware/        # Request/response processing
├── cache/             # Caching framework
├── constants/         # Project-wide constants
├── extensions/        # Django extensions
├── templates/         # Reusable templates
└── templatetags/      # Custom template filters and tags
```

## Module Documentation

For detailed information about each module, see:

- **[Apps](./apps/README.md)** - Reusable Django application packages
- **[Libraries](./lib/README.md)** - Third-party service integrations
- **[Utilities](./utils/README.md)** - Helper functions and utilities
- **[API](./api/README.md)** - REST API patterns and tools
- **[Cache](./cache/README.md)** - Caching framework and patterns
- **[Forms](./forms/README.md)** - Form utilities and base classes
- **[Decorators](./decorators/README.md)** - Function and class decorators
- **[Models](./models/README.md)** - Abstract models and custom fields
- **[Validators](./validators/README.md)** - Validation utilities

## Use Cases

**Hackathons:** Rapidly build production-quality features with pre-built apps and integrations.

**SaaS Applications:** Multi-organization support, billing, and user management out of the box.

**E-commerce:** Stripe payments, inventory management, order processing.

**Content Platforms:** User accounts, organizations, messaging, notifications.

**Marketplaces:** Payment processing, user profiles, organization support.

## Contributing

HTK is designed to be extended. Create custom apps that inherit from abstract base classes and add your own business logic.
