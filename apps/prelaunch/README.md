# Prelaunch App

Early access and pre-launch signup management.

## Quick Start

```python
from htk.apps.prelaunch.models import PrelaunchSignup
from htk.apps.prelaunch.utils import get_unique_signups, is_prelaunch_mode

# Create signup
signup = PrelaunchSignup.objects.create(
    email='user@example.com',
    referral_code='friend123'
)

# Get or create
signup, created = PrelaunchSignup.objects.get_or_create_by_email(
    email='user@example.com'
)

# Grant early access
signup.grant_early_access()

# Check prelaunch mode
if is_prelaunch_mode():
    # Show prelaunch message
    pass
```

## Prelaunch Signup Management

### Create Signups

```python
from htk.apps.prelaunch.models import PrelaunchSignup

# Manual signup
signup = PrelaunchSignup.objects.create(
    email='user@example.com',
    first_name='John',
    last_name='Doe',
    referral_code='code123'
)

# Bulk import
emails = ['user1@example.com', 'user2@example.com', 'user3@example.com']
for email in emails:
    PrelaunchSignup.objects.get_or_create(email=email)
```

### Grant Early Access

```python
from htk.apps.prelaunch.models import PrelaunchSignup

# Grant access to one user
signup = PrelaunchSignup.objects.get(email='user@example.com')
signup.grant_early_access()

# Grant to multiple users
signups = PrelaunchSignup.objects.filter(email__endswith='@company.com')
for signup in signups:
    signup.grant_early_access()

# Bulk grant
PrelaunchSignup.objects.filter(
    signup_date__gte=date(2024, 1, 1)
).update(has_early_access=True)
```

### Track Signups

```python
from htk.apps.prelaunch.utils import get_unique_signups

# Get all unique signups
unique = get_unique_signups()

# Count by day
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

today = timezone.now().date()
week_ago = today - timedelta(days=7)

daily_signups = PrelaunchSignup.objects.filter(
    created__date__gte=week_ago
).values('created__date').annotate(count=Count('id'))
```

## Prelaunch Mode

### Enable/Disable Prelaunch

```python
from htk.apps.prelaunch.utils import is_prelaunch_mode, set_prelaunch_mode

# Check if in prelaunch mode
if is_prelaunch_mode():
    # Restrict access
    pass

# Set prelaunch status
set_prelaunch_mode(True)   # Enable prelaunch
set_prelaunch_mode(False)  # Disable prelaunch
```

### Middleware Protection

```python
from htk.apps.prelaunch.middleware import PrelaunchMiddleware

# In settings.py
MIDDLEWARE = [
    # ... other middleware ...
    'htk.apps.prelaunch.middleware.PrelaunchMiddleware',
]

# When prelaunch is active:
# - Unauthenticated users redirected to prelaunch page
# - Users with early access can proceed
# - Exception paths bypass prelaunch check
```

### Exception Paths

```python
# settings.py
PRELAUNCH_EXCEPTED_PATHS = [
    '/health/',
    '/api/status/',
    '/static/',
    '/media/',
    '/prelaunch/',
]

PRELAUNCH_REDIRECT_URL = '/prelaunch/'
```

## Common Patterns

### Referral System

```python
from htk.apps.prelaunch.models import PrelaunchSignup

# Track referrals
referrer = PrelaunchSignup.objects.get(referral_code='ABC123')
referred = PrelaunchSignup.objects.create(
    email='friend@example.com',
    referred_by=referrer
)

# Get referral count
referral_count = referrer.referred_signups.count()

# Reward referrals
if referrer.referred_signups.filter(has_early_access=True).count() >= 5:
    # Grant premium features
    referrer.grant_special_status()
```

### Waitlist Notifications

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from htk.apps.prelaunch.models import PrelaunchSignup
from htk.apps.notifications.utils import notify

@receiver(post_save, sender=PrelaunchSignup)
def notify_on_signup(sender, instance, created, **kwargs):
    if created:
        # Send confirmation email
        notify(
            instance,
            f'You\'ve been added to the waitlist for {position}',
            channel='email',
            subject='Waitlist Confirmation'
        )

@receiver(post_save, sender=PrelaunchSignup)
def send_access_granted_email(sender, instance, **kwargs):
    if instance.has_early_access:
        notify(
            instance,
            'You now have early access!',
            channel='email',
            subject='Early Access Granted'
        )
```

### Phased Rollout

```python
from htk.apps.prelaunch.models import PrelaunchSignup
from django.utils import timezone
from datetime import timedelta

# Grant access in waves
total_signups = PrelaunchSignup.objects.count()

# Wave 1: First 10%
wave1_count = int(total_signups * 0.1)
wave1 = PrelaunchSignup.objects.filter(
    has_early_access=False
).order_by('created')[:wave1_count]

for signup in wave1:
    signup.has_early_access = True
    signup.save()

# Wave 2: Next 25% after 1 week
wave2_date = timezone.now() - timedelta(days=7)
wave2_count = int(total_signups * 0.25)
wave2 = PrelaunchSignup.objects.filter(
    has_early_access=False,
    created__lte=wave2_date
).order_by('created')[:wave2_count]

for signup in wave2:
    signup.grant_early_access()
```

### Unsubscribe Management

```python
from htk.apps.prelaunch.models import PrelaunchSignup

# Track unsubscribes
signup = PrelaunchSignup.objects.get(email='user@example.com')
signup.is_subscribed = False
signup.save()

# Get active signups
active = PrelaunchSignup.objects.filter(is_subscribed=True)

# Send to active only
for signup in active:
    send_email(signup.email, 'Launch announcement!')
```

## Models

### PrelaunchSignup

```python
class PrelaunchSignup(models.Model):
    email = EmailField(unique=True)
    first_name = CharField(max_length=100, blank=True)
    last_name = CharField(max_length=100, blank=True)
    referral_code = CharField(max_length=20, unique=True)
    referred_by = ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    has_early_access = BooleanField(default=False)
    is_subscribed = BooleanField(default=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
```

## Configuration

```python
# settings.py
PRELAUNCH_ENABLED = True
PRELAUNCH_REDIRECT_URL = '/early-access/'

# Paths that bypass prelaunch check
PRELAUNCH_EXCEPTED_PATHS = [
    '/health/',
    '/api/status/',
    '/static/',
    '/media/',
    '/prelaunch/',
    '/admin/',
]

# Early access paths (accessible with early access)
PRELAUNCH_EARLY_ACCESS_PATHS = []
```

## Best Practices

1. **Use referral codes** - Track referral source
2. **Phased rollout** - Gradually release to manage load
3. **Notify on access** - Send confirmation when granted
4. **Track metrics** - Monitor signup conversion and engagement
5. **Handle unsubscribes** - Respect user preferences
6. **Provide feedback** - Show waitlist position if possible

## Related Modules

- `htk.apps.accounts` - User registration after launch
- `htk.apps.notifications` - Send notifications
- `htk.middleware` - Request filtering
