# Django HTK (Hacktoolkit)

> Production-ready Django toolkit with 29 apps, 47+ integrations, and 24 utility categories for rapid prototyping and scaling.

## Overview

HTK provides reusable Django applications, third-party service integrations, and utility functions. Use what you need—the modular architecture allows selective adoption without unnecessary dependencies.

## Quick Start

Add to `settings.py`:

```python
INSTALLED_APPS = [
    # ... your apps
    'htk.apps.accounts',      # User authentication & profiles
    'htk.apps.notifications',  # Multi-channel notifications
    'htk.apps.organizations',  # Team management
]
```

See individual module documentation for configuration.

## Components at a Glance

### Core Modules

Essential Django utilities organized by function:

| Module | Purpose |
|--------|---------|
| **[admin](admin/README.md)** | Admin customizations and abstract classes |
| **[api](api/README.md)** | REST/JSON API utilities |
| **[cache](cache/README.md)** | Smart caching with descriptors |
| **[models](models/README.md)** | Base model classes and custom fields |
| **[forms](forms/README.md)** | Form classes and widgets |
| **[utils](utils/README.md)** | 24 categories of utility functions |
| **[validators](validators/README.md)** | Data validation helpers |
| **[decorators](decorators/README.md)** | Reusable function decorators |
| **[constants](constants/README.md)** | Centralized application constants |
| **[extensions](extensions/README.md)** | Extended data structures |

### Feature Applications (29)

Pre-built, production-ready apps for common needs:

**User & Organizations**
- [accounts](apps/accounts/README.md) - Authentication, profiles, OAuth
- [organizations](apps/organizations/README.md) - Team and organization management
- [addresses](apps/addresses/README.md) - Address storage and validation
- [invitations](apps/invitations/README.md) - Invitation system

**Communication**
- [notifications](apps/notifications/README.md) - Multi-channel delivery
- [conversations](apps/conversations/README.md) - Direct messaging
- [forums](apps/forums/README.md) - Discussion forums

**Content & Commerce**
- [store](apps/store/README.md) - E-commerce functionality
- [cpq](apps/cpq/README.md) - Configure, Price, Quote
- [customers](apps/customers/README.md) - Customer management
- [bible](apps/bible/README.md) - Bible data and lookup
- [assessments](apps/assessments/README.md) - Quizzes and evaluations
- [feedback](apps/feedback/README.md) - User feedback collection

**Storage & Infrastructure**
- [file_storage](apps/file_storage/README.md) - File uploads
- [blob_storage](apps/blob_storage/README.md) - Binary large object storage
- [kv_storage](apps/kv_storage/README.md) - Key-value storage
- [async_task](apps/async_task/README.md) - Async task handling
- [tokens](apps/tokens/README.md) - Token management

**Features & Configuration**
- [features](apps/features/README.md) - Feature flags and A/B testing
- [url_shortener](apps/url_shortener/README.md) - URL shortening
- [geolocations](apps/geolocations/README.md) - Location services
- [i18n](apps/i18n/README.md) - Internationalization
- [mobile](apps/mobile/README.md) - Mobile app support
- [changelog](apps/changelog/README.md) - Release notes
- [maintenance_mode](apps/maintenance_mode/README.md) - Maintenance windows
- [prelaunch](apps/prelaunch/README.md) - Pre-launch modes
- [sites](apps/sites/README.md) - Multi-site support
- [mp](apps/mp/README.md) - Marketplace functionality

[Complete app documentation →](apps/README.md)

### Service Integrations (47+)

Connect to external services with pre-built integrations:

| Category | Services |
|----------|----------|
| **Cloud** | AWS (S3, EC2, Lambda), Google Cloud, Mapbox, MongoDB, RabbitMQ |
| **Messaging** | Slack, Discord, Mailchimp, Iterable, Plivo, OpenAI, Alexa |
| **Social** | Google OAuth, Facebook, Twitter, LinkedIn, GitHub, Apple Sign In |
| **Payments** | Stripe, Zuora |
| **Data** | Airtable, FullContact, DarkSky, GeoIP |
| **Real Estate** | Zillow, Redfin, Yelp, Indeed, ZipRecruiter, Glassdoor |
| **Other** | Bible APIs (ESV, LiteralWord), QR Codes, Gravatar, Shopify, YouTube |

[Complete integrations documentation →](lib/README.md)

## Documentation

**Choose your path:**

- **[Core modules](admin/README.md)** - Django utilities and helpers
- **[Feature apps](apps/README.md)** - 29 production-ready applications
- **[Integrations](lib/README.md)** - 47+ service connectors
- **[Complete analysis](../htk_analysis.md)** - Comprehensive codebase reference

## Installation

```bash
pip install django-htk
```

## Contributing

Contributions welcome! [Fork the repository](https://github.com/hacktoolkit/htk-django-skeleton), create a feature branch, add tests, and submit a pull request.

## Support

- **Bug reports:** [GitHub Issues](https://github.com/hacktoolkit/htk-django-skeleton/issues)
- **Module docs:** See individual README files
- **Deep dive:** [Full codebase analysis](../htk_analysis.md)

## Notes

- **Author:** [Jonathan Tsai](https://github.com/jontsai)
- **License:** MIT
- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
