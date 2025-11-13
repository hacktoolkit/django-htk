# Constants

Configuration constants for the accounts app, including authentication settings, email templates, social auth providers, and user model references.

## Imports

```python
from htk.apps.accounts.constants import (
    HTK_ACCOUNTS_DEFAULT_DISPLAY_NAME,
    HTK_ACCOUNTS_CONFIRM_EMAIL_URL_NAME,
    HTK_DEFAULT_LOGGED_IN_ACCOUNT_HOME,
    HTK_USER_PROFILE_MODEL,
    HTK_SOCIAL_AUTH_PROVIDERS,
    USERNAME_MAX_LENGTH,
    EMAIL_ACTIVATION_KEY_EXPIRATION_HOURS,
    SocialAuth,
    SOCIAL_AUTHS,
)
```

## Configuration Constants

### URL Settings

- `HTK_ACCOUNTS_CONFIRM_EMAIL_URL_NAME` - URL name for email confirmation view
- `HTK_API_USERS_FOLLOW_URL_NAME` - URL name for follow user endpoint
- `HTK_API_USERS_UNFOLLOW_URL_NAME` - URL name for unfollow user endpoint
- `HTK_DEFAULT_LOGGED_IN_ACCOUNT_HOME` - Default home URL for logged-in users
- `HTK_ACCOUNTS_REGISTER_SOCIAL_LOGIN_URL_NAME` - Social login registration URL
- `HTK_ACCOUNTS_REGISTER_SOCIAL_EMAIL_URL_NAME` - Social email registration URL
- `HTK_ACCOUNTS_REGISTER_SOCIAL_ALREADY_LINKED_URL_NAME` - Already linked account URL
- `HTK_ACCOUNTS_REGISTER_SOCIAL_EMAIL_AND_TERMS_URL_NAME` - Email and terms registration URL
- `HTK_ACCOUNTS_RESET_PASSWORD_URL_NAME` - Password reset URL
- `HTK_ACCOUNTS_RESEND_CONFIRMATION` - Resend confirmation email URL

### User Settings

- `HTK_ACCOUNTS_DEFAULT_DISPLAY_NAME` - Default name for new users (default: `'User'`)
- `HTK_USER_PROFILE_MODEL` - Custom user profile model (default: `None`)
- `HTK_VALID_USERNAME_REGEX` - Pattern for valid usernames: `r'^[A-Za-z0-9_-]{1,30}$'`
- `HTK_USERNAME_HELP_TEXT` - Help text for username field
- `USERNAME_MAX_LENGTH` - Maximum username length (30 characters)

### Authentication & Security

- `HTK_ACCOUNTS_CHANGE_PASSWORD_UPDATE_SESSION_AUTH_HASH` - Update session hash on password change (default: `True`)
- `HTK_USER_ID_XOR` - XOR key for encoding user IDs (default: `314159265`)
- `HTK_USER_TOKEN_AUTH_ENCRYPTION_KEY` - Key for token auth encryption
- `HTK_USER_TOKEN_AUTH_EXPIRES_MINUTES` - Token auth expiration in minutes (default: `15`)

### Email Settings

- `HTK_ACCOUNT_EMAIL_SUBJECT_ACTIVATION` - Subject for activation email
- `HTK_ACCOUNT_EMAIL_SUBJECT_PASSWORD_CHANGED` - Subject for password change email
- `HTK_ACCOUNT_EMAIL_SUBJECT_PASSWORD_RESET` - Subject for password reset email
- `HTK_ACCOUNT_EMAIL_SUBJECT_WELCOME` - Subject for welcome email
- `HTK_ACCOUNT_EMAIL_BCC_ACTIVATION` - BCC activation emails (default: `True`)
- `HTK_ACCOUNT_EMAIL_BCC_WELCOME` - BCC welcome emails (default: `True`)
- `HTK_ACCOUNT_ACTIVATION_REMINDER_EMAIL_TEMPLATE` - Template for activation reminder

### Registration & Activation

- `HTK_ACCOUNT_ACTIVATE_UPON_REGISTRATION` - Auto-activate accounts on registration (default: `False`)
- `HTK_ACCOUNTS_REGISTER_SET_PRETTY_USERNAME_FROM_EMAIL` - Generate username from email (default: `False`)
- `HTK_ACCOUNTS_SOCIAL_AUTO_ASSOCIATE_BACKENDS` - Backends for auto-linking social accounts (default: `[]`)
- `EMAIL_ACTIVATION_KEY_EXPIRATION_HOURS` - Activation key expiration time (48 hours)
- `EMAIL_ACTIVATION_KEY_REUSE_THRESHOLD_HOURS` - Threshold before activation key can be reused

### User Attributes & Social Auth

- `HTK_USER_ATTRIBUTE_DEFAULTS` - Default attributes for new users (default: `{}`)
- `HTK_SOCIAL_AUTH_PROVIDERS` - List of available social auth providers
- `HTK_SOCIAL_AUTH_LOGIN_PROVIDERS` - List of providers allowed for login

## Classes

### SocialAuth

Dataclass representing a social authentication provider:

```python
from htk.apps.accounts.constants import SocialAuth, SOCIAL_AUTHS

# Access defined social auths
for auth in SOCIAL_AUTHS:
    print(f"{auth.name}: {auth.provider}")

# Create custom SocialAuth instance
custom_auth = SocialAuth(
    provider='custom-provider',
    name='Custom',
    bg_color='#ff0000',
    fa_icon='fa-solid fa-custom'
)
```

Available providers in `SOCIAL_AUTHS`: Apple, Discord, Facebook, Fitbit, GitHub, Google, LinkedIn, Strava, Twitter, Withings

## Search Constants

- `DEFAULT_NUM_SEARCH_RESULTS` - Default number of search results (20)
