# Models

## Overview

This models module defines Django models that represent the database schema. Models define fields, relationships, methods, and metadata for objects persisted to the database.

## Quick Start

### Query Models

```python
from htk.apps.prelaunch.models import PrelaunchSignup

# Get all signups
signups = PrelaunchSignup.objects.all()

# Filter by condition
active = PrelaunchSignup.objects.filter(is_active=True)

# Get single signup
signup = PrelaunchSignup.objects.get(id=1)  # Raises DoesNotExist if not found

# Get or None
signup = PrelaunchSignup.objects.filter(email='user@example.com').first()  # Returns None if not found
```

### Create Objects

```python
from htk.apps.prelaunch.models import PrelaunchSignup

# Create and save
signup = PrelaunchSignup.objects.create(
    email='user@example.com',
    ip_address='192.168.1.1'
)

# Create instance, modify, then save
signup = PrelaunchSignup(email='user@example.com')
signup.save()

# Bulk create
signups = PrelaunchSignup.objects.bulk_create([
    PrelaunchSignup(email='user1@example.com'),
    PrelaunchSignup(email='user2@example.com'),
])
```

## Model Fields

Models include various field types:

- **CharField** - Text (limited length)
- **TextField** - Long text
- **IntegerField** - Integer numbers
- **ForeignKey** - Relationship to another model
- **ManyToManyField** - Many-to-many relationship
- **DateTimeField** - Date and time
- **BooleanField** - True/False

### Field Options

```python
from htk.apps.prelaunch.models import PrelaunchSignup

# PrelaunchSignup fields include:
# - email: EmailField (unique, max_length=254)
# - is_active: BooleanField (default=True)
# - created: DateTimeField (auto_now_add=True)
# - updated: DateTimeField (auto_now=True)
# - ip_address: GenericIPAddressField (optional)

# Query by field options
recently_created = PrelaunchSignup.objects.filter(
    created__gte=timezone.now() - timedelta(days=7)
)
```

## Relationships

### Foreign Key

One-to-many relationship:

```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
```

### Many-to-Many

Many-to-many relationship:

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, related_name='articles')
```

## Properties and Methods

### @property

Computed property example:

```python
from htk.apps.prelaunch.models import PrelaunchSignup

signup = PrelaunchSignup.objects.first()

# Use computed properties if defined on model
# (check PrelaunchSignup.models for available @property methods)
if hasattr(signup, 'display_name'):
    print(signup.display_name)
```

## Querysets

### Filtering

```python
from htk.apps.prelaunch.models import PrelaunchSignup
from django.utils import timezone
from datetime import timedelta

# Exact match
PrelaunchSignup.objects.filter(is_active=True)

# Greater than - signups from last week
PrelaunchSignup.objects.filter(created__gt=timezone.now() - timedelta(days=7))

# Contains - email domain search
PrelaunchSignup.objects.filter(email__icontains='@example.com')

# In list - specific statuses
PrelaunchSignup.objects.filter(is_active__in=[True, False])
```

### Ordering

```python
from htk.apps.prelaunch.models import PrelaunchSignup

# Ascending - oldest first
PrelaunchSignup.objects.all().order_by('created')

# Descending - newest first
PrelaunchSignup.objects.all().order_by('-created')
```

## Best Practices

1. **Use QuerySets** - Dont fetch unnecessary data
2. **Select related** - Use `select_related()` for ForeignKey
3. **Prefetch related** - Use `prefetch_related()` for ManyToMany
4. **Index fields** - Add `db_index=True` to frequently filtered fields
5. **Use choices** - For fields with limited values
6. **Document fields** - Use `help_text`
7. **Add Meta class** - Configure ordering, permissions, verbose names
