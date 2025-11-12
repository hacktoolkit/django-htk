# HTK Accounts App

> User authentication, account management, and profile management for HTK applications.

## Purpose

The accounts app extends Django's authentication system with email verification, password management, and user profiles. It supports OAuth integration, profile customization, and security features like rate limiting and two-factor authentication.

## Quick Start

```python
from django.contrib.auth.models import User
from htk.apps.accounts.models import UserProfile

# Create user with profile
user = User.objects.create_user(
    username='jane_doe',
    email='jane@example.com',
    password='secure_password'
)
profile = user.userprofile
```

## Key Components

| Component | Purpose |
|-----------|---------|
| **UserProfile** | Extend User model with bio, phone, avatar |
| **EmailConfirmation** | Token-based email verification |
| **RegistrationForm** | User signup with validation |
| **PasswordResetForm** | Secure password reset flow |

## Common Patterns

### Email Verification

```python
from htk.apps.accounts.models import EmailConfirmation

confirmation = EmailConfirmation.objects.get(token=token)
if confirmation.is_valid():
    confirmation.confirm()
```

### Password Reset

```python
from django.contrib.auth.views import PasswordResetView
from htk.apps.accounts.forms import PasswordResetForm

class CustomResetView(PasswordResetView):
    form_class = PasswordResetForm
```

### Profile Updates

```python
profile = request.user.userprofile
profile.bio = 'Updated bio'
profile.save()
```

## Configuration

Add to `settings.py`:

```python
HTK_ACCOUNT_EMAIL_VERIFICATION_TIMEOUT = 86400  # 24 hours
HTK_ACCOUNT_PASSWORD_MIN_LENGTH = 8
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'your-key'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'your-secret'
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/auth/register/` | POST | Register new user |
| `/api/auth/login/` | POST | Login user |
| `/api/accounts/profile/` | GET | Get profile |
| `/api/accounts/profile/` | PATCH | Update profile |
| `/api/auth/password-reset/` | POST | Initiate password reset |

## Best Practices

- **Email verification first** - Verify before granting full access
- **Time-limited tokens** - Use 24-hour expiration for security tokens
- **Rate limiting** - Protect login, password reset, and resend endpoints
- **Account recovery** - Provide multiple recovery methods
- **HTTPS + secure cookies** - Require secure connection in production

## Testing

```python
from django.test import TestCase
from django.contrib.auth.models import User

class AccountsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )

    def test_profile_created(self):
        """Verify profile created with user."""
        self.assertTrue(hasattr(self.user, 'userprofile'))
```

## Related Modules

- `htk.apps.notifications` - Send account notifications
- `htk.apps.invitations` - Invite users to join
- `htk.apps.organizations` - Team membership management
- `htk.api.auth` - REST API authentication helpers

## References

- [Django Authentication](https://docs.djangoproject.com/en/stable/topics/auth/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
