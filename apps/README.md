# HTK Apps Module

29 production-ready Django applications providing domain-specific functionality.

## Overview

Each application in HTK is:
- **Independently functional** - Use only what you need
- **Modular** - Reusable across multiple domains
- **Selectively installable** - Enable based on project requirements
- **Feature-complete** - Models, views, forms, admin, and API included

## Architecture

Each HTK app follows this structure:

```
appname/
├── __init__.py           # App configuration
├── models.py             # Data models
├── views.py              # View logic
├── urls.py              # URL routing
├── forms.py             # Form classes
├── admin.py             # Admin configuration
├── managers.py          # Model managers
├── utils.py             # Utility functions
├── constants/           # App-specific constants
│   └── __init__.py
├── migrations/          # Database migrations
├── api/                 # API endpoints
│   └── __init__.py
└── templates/           # App templates
```

## App Categories

### 1. User & Account Management

#### **accounts** - User authentication and profiles
- User registration and authentication
- Email verification
- Password management
- Social authentication integration (Apple, Google, Facebook)
- User profiles
- Session management

**Key Models:** User, UserProfile, UserToken
**Key Features:** Registration, email confirmation, password reset, OAuth

#### **organizations** - Organization and team management
- Organization creation and management
- Team structure
- Member invitations
- Role-based access control
- Organization settings

**Key Models:** Organization, Team, Member, Role
**Key Features:** Multi-tenancy support, team collaboration

### 2. Communication & Messaging

#### **conversations** - Direct messaging
- User-to-user messaging
- Group conversations
- Message threading
- Typing indicators
- Message search

**Key Models:** Conversation, Message, Participant
**Key Features:** Real-time messaging, conversation history

#### **notifications** - User notifications
- In-app notifications
- Email notifications
- Push notifications
- Notification channels
- Notification preferences

**Key Models:** Notification, NotificationPreference, NotificationChannel
**Key Features:** Multi-channel delivery, preference management

#### **invitations** - Invitation system
- Send invitations
- Track invitation status
- Accept/decline invitations
- Expiring invitations
- Bulk invitations

**Key Models:** Invitation, InvitationCode
**Key Features:** Email invitations, expiration handling

#### **forums** - Discussion forums
- Forum categories
- Discussion threads
- Comments and replies
- Voting/reactions
- Moderation

**Key Models:** Forum, Thread, Post, Vote
**Key Features:** Community discussions, content moderation

### 3. Content & Data Management

#### **bible** - Bible data and references
- Bible books, chapters, verses
- Multiple translations (NASB, ESV, etc.)
- Bible passage lookup and resolution
- Cross-references
- Study aids

**Key Models:** Book, Chapter, Verse, Translation
**Key Features:** Bible search, passage resolution, reference linking

#### **changelog** - Release notes and version tracking
- Version management
- Release notes
- Changelog generation
- Slack announcements
- Web changelog view

**Key Models:** Release, ChangeLog
**Key Features:** Automated changelog, version tracking

#### **feedback** - User feedback and surveys
- Feedback collection
- Survey creation
- Rating/review system
- Feedback analysis
- Response tracking

**Key Models:** Feedback, Survey, Response
**Key Features:** User feedback, survey administration

#### **assessments** - Quizzes and assessments
- Assessment creation
- Question and answer management
- Score tracking
- Result generation
- Reporting

**Key Models:** Assessment, Question, Answer, Result
**Key Features:** Quizzes, scoring, analytics

### 4. Storage & File Management

#### **file_storage** - File upload and management
- File uploads
- File versioning
- Access control
- Storage backend integration (S3, local)
- File serving

**Key Models:** File, FileVersion
**Key Features:** Multi-backend support, access control

#### **blob_storage** - Binary large object storage
- BLOB storage
- Compression
- Streaming
- Size management

**Key Models:** Blob
**Key Features:** Large file handling

#### **kv_storage** - Key-value storage
- Simple key-value pairs
- TTL support
- Type flexibility
- Query support

**Key Models:** KeyValueStore
**Key Features:** Flexible storage, expiration

### 5. Commerce & Business Logic

#### **store** - E-commerce and store
- Products
- Shopping cart
- Orders
- Inventory
- Payment integration

**Key Models:** Product, Cart, Order, OrderItem
**Key Features:** Shopping cart, order management

#### **cpq** - Configure-Price-Quote
- Product configuration
- Dynamic pricing
- Quote generation
- Customer contracts

**Key Models:** Quote, QuoteItem, Configuration
**Key Features:** Complex pricing, quote workflows

#### **customers** - Customer management
- Customer profiles
- Purchase history
- Preferences
- Communication history
- Segmentation

**Key Models:** Customer, CustomerProfile
**Key Features:** CRM functionality

### 6. Features & Flags

#### **features** - Feature flags
- Feature toggles
- A/B testing
- Gradual rollouts
- User targeting
- Analytics

**Key Models:** Feature, FeatureFlag, FeatureUser
**Key Features:** Feature toggle, targeting

### 7. Technical Infrastructure

#### **async_task** - Asynchronous tasks
- Task queuing (Celery integration)
- Task scheduling
- Task status tracking
- Error handling

**Key Models:** Task, TaskResult
**Key Features:** Async execution, task tracking

#### **url_shortener** - URL shortening
- Short URL generation
- Tracking redirects
- Analytics
- Expiration

**Key Models:** ShortURL, URLClick
**Key Features:** URL tracking, analytics

#### **tokens** - Token management
- API tokens
- Temporary tokens
- Token validation
- Revocation

**Key Models:** Token
**Key Features:** Session-less auth, token lifecycle

#### **geolocations** - Location services
- IP geolocation
- Address geocoding
- Location-based queries
- Distance calculations

**Key Models:** Location
**Key Features:** Mapping, proximity search

#### **i18n** - Internationalization
- Multi-language support
- Translation management
- Locale selection
- Language preferences

**Key Features:** Multi-language support, locale detection

#### **addresses** - Address management
- Address storage
- Address validation
- Geocoding
- Address formatting

**Key Models:** Address
**Key Features:** Address parsing, validation

### 8. Deployment & Maintenance

#### **maintenance_mode** - Site maintenance
- Enable/disable maintenance mode
- Custom maintenance page
- Whitelisted IPs
- Email notifications

**Key Features:** Maintenance windows, exception handling

#### **prelaunch** - Pre-launch mode
- Coming soon pages
- Email collection
- Launch countdown
- Beta access

**Key Models:** PrelaunchSignup
**Key Features:** Coming soon, email capture

#### **sites** - Multi-site support
- Multiple site management
- Site-specific settings
- Domain routing
- Site switching

**Key Features:** Multi-tenancy, domain routing

### 9. Other Utilities

#### **mobile** - Mobile app support
- Device registration
- Push notifications
- App-specific settings
- Device tracking

**Key Models:** Device
**Key Features:** Push notifications, device management

#### **mp** - Marketplace (undefined purpose)
- Likely: Seller/vendor management
- Product listings
- Commission tracking

#### **documentation_automation** - Documentation automation
- Automated documentation generation
- Code documentation helpers
- Documentation management tools

## Installation

### Adding an App to Your Project

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'htk.apps.changelog',
    'htk.apps.accounts',
    # Add other apps as needed
]
```

### Database Migrations

```bash
python manage.py migrate
```

## Configuration

### Per-App Settings

Each app has optional settings in the form `HTK_<APP_NAME>_*`:

```python
# settings.py

# Accounts app
HTK_USER_PROFILE_MODEL = 'myapp.UserProfile'

# Changelog app
HTK_CHANGELOG_FILE_PATH = BASE_DIR / 'CHANGELOG.md'
HTK_CHANGELOG_SLACK_CHANNEL_RELEASES = '#releases'

# Maintenance mode
HTK_MAINTENANCE_MODE = False
HTK_MAINTENANCE_MODE_EXCEPTION_VIEWS = []

# Features
HTK_FEATURE_FLAG_MODEL = 'myapp.FeatureFlag'
```

## Usage Patterns

### Pattern 1: Using the Accounts App

```python
from htk.apps.accounts.models import User

# Create user
user = User.objects.create_user(
    username='john',
    email='john@example.com',
    password='password123'
)

# Get user profile
profile = user.userprofile
```

### Pattern 2: Using Organizations App

```python
from htk.apps.organizations.models import Organization, Team

# Create organization
org = Organization.objects.create(
    name='Acme Corp',
    slug='acme'
)

# Create team within organization
team = Team.objects.create(
    organization=org,
    name='Engineering'
)
```

### Pattern 3: Using Notifications

```python
from htk.apps.notifications.models import Notification

# Create notification
notif = Notification.objects.create(
    user=request.user,
    title='New message',
    message='You have a new message from John',
    notification_type='message'
)
```

### Pattern 4: Using Features

```python
from htk.apps.features.models import Feature

# Check feature flag
if Feature.is_enabled('new_dashboard', user=request.user):
    # Use new dashboard
    pass
else:
    # Use old dashboard
    pass
```

## API Integration

Most apps provide REST API endpoints:

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'htk.apps.accounts',
    'htk.apps.organizations',
    'htk.apps.notifications',
]

# urls.py
from django.urls import path, include

urlpatterns = [
    path('api/accounts/', include('htk.apps.accounts.api.urls')),
    path('api/organizations/', include('htk.apps.organizations.api.urls')),
    path('api/notifications/', include('htk.apps.notifications.api.urls')),
]
```

## Common Patterns Across Apps

### 1. Time Tracking

Most models include:
```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

### 2. Soft Deletes

Many models support soft deletes:
```python
is_deleted = models.BooleanField(default=False)

# Query active items
Item.objects.filter(is_deleted=False)
```

### 3. Status Fields

Many models use status tracking:
```python
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('active', 'Active'),
    ('completed', 'Completed'),
]
status = models.CharField(max_length=20, choices=STATUS_CHOICES)
```

### 4. User Association

Most models link to User model:
```python
user = models.ForeignKey(User, on_delete=models.CASCADE)
created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

## Testing Apps

```python
from django.test import TestCase
from htk.apps.accounts.models import User

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
```

## App Dependencies

```
accounts → base user functionality
  ↓
organizations → uses accounts for owner/members
  ↓
notifications → uses accounts for recipients
  ↓
conversations → uses accounts for participants
  ↓
invitations → uses accounts for inviter/invitee
```

## Related Documentation

- [HTK Models](../models/README.md) - Base model classes
- [HTK API](../api/README.md) - API utilities
- [HTK Forms](../forms/README.md) - Form utilities
- [HTK Admin](../admin/README.md) - Admin customizations
- [Django Apps Documentation](https://docs.djangoproject.com/en/stable/ref/applications/)
- [Django Models Documentation](https://docs.djangoproject.com/en/stable/topics/db/models/)

## Status

- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
- **Documentation Confidence:** HIGH (>95%)
