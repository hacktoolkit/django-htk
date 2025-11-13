# Feedback App

User feedback and review collection system.

## Quick Start

```python
from htk.apps.feedback.models import Feedback

# Submit feedback
feedback = Feedback.objects.create(
    user=request.user,
    message='Great product!',
    rating=5,
    category='general'
)

# Get user's feedback
user_feedback = Feedback.objects.filter(user=request.user)

# Query by category
feature_requests = Feedback.objects.filter(category='feature_request')
```

## Submitting Feedback

### Basic Feedback

```python
from htk.apps.feedback.models import Feedback

# Simple feedback
feedback = Feedback.objects.create(
    user=user,
    message='Love the new design!',
    rating=5
)

# Or without user
anonymous_feedback = Feedback.objects.create(
    email='user@example.com',
    message='Found a bug',
    rating=2,
    category='bug'
)
```

### Categorized Feedback

```python
from htk.apps.feedback.models import Feedback

# Categorize feedback
categories = ['general', 'bug', 'feature_request', 'support']

bug_report = Feedback.objects.create(
    user=user,
    message='Image upload broken',
    category='bug',
    rating=1
)

feature_req = Feedback.objects.create(
    user=user,
    message='Please add dark mode',
    category='feature_request',
    rating=4
)
```

## Common Patterns

### Feedback Analytics

```python
from django.db.models import Avg, Count
from htk.apps.feedback.models import Feedback

# Average rating
avg_rating = Feedback.objects.aggregate(
    avg=Avg('rating')
)['avg']

# Count by category
feedback_by_category = Feedback.objects.values('category').annotate(
    count=Count('id'),
    avg_rating=Avg('rating')
).order_by('-count')

# Get top rated feedback
top_feedback = Feedback.objects.order_by('-rating')[:10]

# Recent feedback
recent = Feedback.objects.order_by('-created')[:20]
```

### Feedback Dashboard

```python
from django.db.models import Avg, Count, Q
from htk.apps.feedback.models import Feedback
from django.utils import timezone
from datetime import timedelta

# Last 30 days stats
cutoff = timezone.now() - timedelta(days=30)
recent_feedback = Feedback.objects.filter(created__gte=cutoff)

stats = {
    'total': recent_feedback.count(),
    'avg_rating': recent_feedback.aggregate(avg=Avg('rating'))['avg'],
    'bugs': recent_feedback.filter(category='bug').count(),
    'features': recent_feedback.filter(category='feature_request').count(),
}
```

### Filter by Rating

```python
from htk.apps.feedback.models import Feedback

# Get positive feedback
positive = Feedback.objects.filter(rating__gte=4)

# Get negative feedback
negative = Feedback.objects.filter(rating__lte=2)

# Get critical issues
critical = Feedback.objects.filter(
    category='bug',
    rating__lte=2
)
```

### Integration with Notifications

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from htk.apps.feedback.models import Feedback
from htk.apps.notifications.utils import notify

@receiver(post_save, sender=Feedback)
def notify_team_on_feedback(sender, instance, created, **kwargs):
    if created:
        # Notify team on new feedback
        if instance.category == 'bug':
            notify(
                admin_users,
                f'Bug report: {instance.message}',
                channel='slack'
            )
        elif instance.category == 'feature_request':
            notify(
                product_team,
                f'Feature request: {instance.message}',
                channel='email'
            )
```

## Models

### Feedback

```python
class Feedback(models.Model):
    user = ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    email = EmailField(blank=True)
    message = TextField()
    rating = IntegerField(default=0)  # 1-5 stars
    category = CharField(max_length=50, default='general')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    is_resolved = BooleanField(default=False)
```

## API Views

### Submit Feedback

```
POST /feedback/submit/
Content-Type: application/json

{
    "message": "Great product!",
    "rating": 5,
    "category": "general"
}
```

### Get Feedback History

```
GET /feedback/my-feedback/
```

Returns user's feedback history with ratings and dates.

## Configuration

```python
# settings.py
FEEDBACK_CATEGORIES = [
    ('general', 'General Feedback'),
    ('bug', 'Bug Report'),
    ('feature_request', 'Feature Request'),
    ('support', 'Support Issue'),
]

FEEDBACK_ENABLED = True
FEEDBACK_RATING_MIN = 1
FEEDBACK_RATING_MAX = 5

# Notification settings
FEEDBACK_NOTIFY_ON_CRITICAL = True  # Notify team on low ratings
FEEDBACK_CRITICAL_THRESHOLD = 2  # Rating threshold
```

## Best Practices

1. **Categorize feedback** - Use categories for organization
2. **Track ratings** - Use 1-5 star system for quantitative data
3. **Include timestamps** - Track when feedback was submitted
4. **Allow anonymous feedback** - Don't require user account
5. **Follow up on bugs** - Mark as resolved when fixed
6. **Analyze trends** - Review feedback regularly
7. **Notify team** - Alert relevant teams of critical issues
