# HTK Accounts Utils

Utilities for user account management, authentication, email handling, encryption, and user lookups.

## Functions by Category

### Authentication (5 functions)

**login_authenticated_user(request, authenticated_user, backend=None)**
- Logs in an authenticated user and updates locale info from request
- Updates Iterable notifications if enabled

**get_user_token_auth_token(user, expires_minutes=None)**
- Generates a token for direct user login (typically for email links)
- Returns base64-encoded JSON with encrypted user ID, expiration, and hash

**validate_user_token_auth_token(token)**
- Validates a user token-auth token
- Returns tuple: `(user, is_valid)` where user is None if invalid

**validate_reset_password_token(uid_base36, token)**
- Validates Django password reset token
- Returns User if valid, None otherwise

**reset_user_password(request, user, new_password1, new_password2=None, email_template=None)**
- Resets user password with form validation
- Returns tuple: `(success, updated_user, form)`

### User Lookup (7 functions)

**get_user_by_username(username, UserModel=None)**
- Gets user by exact username match
- Returns None if not found

**get_user_by_email(email)**
- Gets user by confirmed email or active user email
- Raises `NonUniqueEmail` if multiple confirmed emails exist

**get_user_by_email_with_retries(email, max_attempts=4)**
- Retries `get_user_by_email()` with exponential backoff
- Mitigates race conditions during account creation

**get_incomplete_signup_user_by_email(email)**
- Gets inactive user by unconfirmed email
- Returns None if not found or data inconsistency

**get_user_by_id(user_id)**
- Gets user by ID
- Returns None if not found

**get_users_by_id(user_ids, strict=False, preserve_ordering=False)**
- Gets list of users by IDs
- If strict=True, all IDs must exist or None returned

**get_user_emails_by_id(user_email_ids, strict=False)**
- Gets list of UserEmail objects by IDs
- Returns partial list or None based on strict mode

### User Creation (6 functions)

**create_user(first_name, last_name, email, username_prefix=None, set_password=True)**
- Creates new user with optional custom username prefix
- Associates user with email and generates random password if set_password=True
- Returns tuple: `(user, password)`

**set_random_password(user, password_length=16)**
- Sets random password using hex UUID
- Returns generated password

**authenticate_user(request, username, password)**
- Authenticates user by username and password
- Returns authenticated user or None

**authenticate_user_by_email(request, email, password)**
- Authenticates user by email and password
- Looks up user by email first

**authenticate_user_by_username_email(request, username_email, password)**
- Authenticates user by username or email (auto-detects)
- Returns authenticated user or None

**authenticate_user_by_basic_auth_credentials(request, credentials)**
- Authenticates user from base64-encoded "username:password"
- Returns authenticated user or None

### Email Management (4 functions)

**get_user_email(user, email, is_confirmed=True)**
- Gets UserEmail object for user and email
- Returns None if not found

**associate_user_email(user, email, replacing=None, domain=None, email_template=None, email_subject=None, email_sender=None, confirmed=False)**
- Associates email with user, sends activation email if needed
- Handles email conflicts and notifies about updates
- Returns UserEmail or None

**extract_user_email(username_email)**
- Gets user from username or email string
- Auto-detects email format
- Returns tuple: `(user, email)`

**notify_user_email_update(user, old_email, new_email)**
- Notifies Iterable of email change if enabled

### Encryption (3 functions)

**encrypt_uid(user)**
- Encrypts user ID using XOR key
- Returns base36-encoded encrypted ID

**decrypt_uid(encrypted_uid)**
- Decrypts user ID from base36 string
- Returns integer user ID

**resolve_encrypted_uid(encrypted_uid)**
- Gets User object from encrypted UID
- Returns None if invalid or not found

### Query/Lookup (6 functions)

**get_all_users(active=True)**
- Gets all users, optionally filtered by active status
- Returns QuerySet

**get_inactive_users()**
- Gets all inactive users
- Returns QuerySet

**get_users_with_attribute_value(key, value, as_bool=False, active=True)**
- Gets users with attribute value match
- Optionally converts value to boolean

**get_users_currently_at_local_time(start_hour, end_hour, isoweekdays=None, active=True)**
- Gets users whose current local time is in range
- Optional day of week filtering (Monday=1, Sunday=7)

**get_users_with_no_confirmed_emails()**
- Gets users with no confirmed email addresses
- Returns QuerySet

**get_duplicate_emails()**
- Sanity check utility finding duplicate emails in database
- Returns sorted list of duplicate email addresses

### Utility (7 functions)

**get_user_profile_model()**
- Resolves HTK_USER_PROFILE_MODEL setting
- Returns model class

**email_to_username_hash(email)**
- Converts email to base64-encoded SHA256 hash (max length from constant)
- Case-insensitive, handles internationalized emails

**email_to_username_pretty_unique(email)**
- Converts email to human-readable unique username
- Extracts handle from email, appends hash if needed

**get_local_time(dt=None, user=None)**
- Converts datetime to user's local timezone
- Uses current authenticated user if not specified

**localized_time_for_user(naive_dt, user=None)**
- Attaches timezone to naive datetime for user
- Useful for processing user-generated content timestamps

**create_missing_user_profiles()**
- Creates missing UserProfile objects for existing users
- One-time migration utility

**get_social_auth_for_user(user, provider)**
- Gets first UserSocialAuth for user and provider
- Returns None if not found

**get_social_auths_for_user(user, provider=None)**
- Gets UserSocialAuth objects for user
- Optionally filters by provider
- Returns QuerySet

## Common Imports

```python
from htk.apps.accounts.utils import (
    login_authenticated_user,
    get_user_by_email,
    authenticate_user_by_email,
    create_user,
    encrypt_uid,
    resolve_encrypted_uid,
)
```
