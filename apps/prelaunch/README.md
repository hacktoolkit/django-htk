# Prelaunch App

> Early access management, waitlist, and feature gating for pre-launch applications.

## Purpose

The prelaunch app provides early access, waitlist, and referral functionality for applications not yet publicly available. It enables invitation-based access, waitlist management with position tracking, referral incentives, and gradual feature rollout.

## Quick Start

```python
from htk.apps.prelaunch.models import PrelaunchWaitlist, PrelaunchInvitation
from datetime import timedelta
from django.utils import timezone

# Add to waitlist
entry = PrelaunchWaitlist.objects.create(
    email='interested@example.com',
    name='John Doe',
    metadata={'location': 'San Francisco'}
)

# Send invitation
expires_at = timezone.now() + timedelta(days=30)
invitation = PrelaunchInvitation.objects.create(
    email='user@example.com',
    expires_at=expires_at
)

# Check access via invitation code
if invitation.is_valid() and not invitation.is_expired():
    invitation.use()
    request.session['prelaunch_access'] = True
```

## Key Components

| Component | Purpose |
|-----------|---------|
| **PrelaunchInvitation** | Individual early access invitation with code and expiry |
| **PrelaunchWaitlist** | Waitlist entry with position, referral code, interests |
| **PrelaunchConfig** | Global prelaunch settings and feature gating |

## Common Patterns

### Waitlist with Position Tracking

```python
from htk.apps.prelaunch.models import PrelaunchWaitlist

# Add user to waitlist
entry = PrelaunchWaitlist.objects.create(
    email='user@example.com',
    name='John Doe'
)

# Get position and referral info
position = entry.get_position()
referral_url = entry.get_referral_url()

# Bulk invite top N users
for entry in PrelaunchWaitlist.objects.all()[:100]:
    entry.invite()
```

### Referral System

```python
def get_referral_stats(email):
    """Get user's referral statistics"""
    entry = PrelaunchWaitlist.objects.get(email=email)
    return {
        'referral_code': entry.referral_code,
        'referral_url': entry.get_referral_url(),
        'count': entry.referral_count,
        'position': entry.get_position(),
    }
```

### Feature Gating with Prelaunch Check

```python
from django.http import HttpResponse

def gated_feature(request):
    """Feature only accessible during prelaunch"""
    if not request.user.prelaunch_access:
        return HttpResponse("Coming soon", status=403)
    # Feature implementation
    return render(request, 'feature.html')
```

## Configuration

```python
# settings.py
HTK_PRELAUNCH_ENABLED = True
HTK_PRELAUNCH_REQUIRE_APPROVAL = True
HTK_PRELAUNCH_INVITATION_EXPIRY_DAYS = 30
HTK_PRELAUNCH_WAITLIST_LIMIT = 10000
HTK_PRELAUNCH_MAINTENANCE_MESSAGE = "Coming soon..."

# Feature flags
HTK_PRELAUNCH_FEATURES = {
    'api_v2': False,
    'mobile_app': False,
    'advanced_analytics': False,
}
```

## API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /api/prelaunch/waitlist/` | Join waitlist |
| `GET /api/prelaunch/waitlist/status/` | Get status and position |
| `POST /api/prelaunch/referral/` | Get referral link |
| `GET /api/prelaunch/check-invite/` | Verify invitation code |
| `POST /api/prelaunch/accept-invite/` | Accept invitation |

## Best Practices

- **Track signup source** - Understand where waitlist traffic comes from
- **Segment by interests** - Prioritize users interested in specific features
- **Incentivize referrals** - Reward referrers with priority access
- **Send updates regularly** - Keep users engaged with position and feature previews
- **Set appropriate expiry** - Balance security with user experience (30 days typical)

## Testing

```python
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from htk.apps.prelaunch.models import PrelaunchInvitation, PrelaunchWaitlist

class PrelaunchTestCase(TestCase):
    def test_invitation_validity(self):
        """Test invitation expiration"""
        expires_at = timezone.now() + timedelta(days=1)
        inv = PrelaunchInvitation.objects.create(
            email='test@example.com', expires_at=expires_at
        )
        self.assertTrue(inv.is_valid())

    def test_waitlist_position(self):
        """Test position tracking"""
        for i in range(5):
            PrelaunchWaitlist.objects.create(email=f'user{i}@test.com')
        user = PrelaunchWaitlist.objects.get(email='user2@test.com')
        self.assertEqual(user.get_position(), 3)
```

## Related Apps

- `htk.apps.accounts` - User accounts
- `htk.apps.invitations` - General invitation system
- `htk.apps.notifications` - Email notifications

## References

- [Prelaunch Strategy](https://www.productlaunch.com/)
- [Waitlist Best Practices](https://neilpatel.com/blog/waitlist/)

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
