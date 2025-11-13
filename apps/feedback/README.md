# Feedback App

User feedback and review collection.

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
```

## Views

```python
# POST /feedback/submit/
# Submit user feedback
```

## Models

- **`Feedback`** - User feedback with rating

## Configuration

```python
# settings.py
FEEDBACK_CATEGORIES = ['general', 'bug', 'feature_request', 'support']
```

## Related Modules

- `htk.apps.accounts` - User tracking
