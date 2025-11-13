# Models

Django ORM models for database schema and queries.

## Overview

This module defines Django models that represent the database schema. Models define fields, relationships, methods, and metadata for objects persisted to the database.

## Quick Start

### Query Models

```python
from htk.apps.prelaunch.models.models import Item

# Get all objects
items = Item.objects.all()

# Filter by condition
active = Item.objects.filter(is_active=True)

# Get single object
item = Item.objects.get(id=1)  # Raises DoesNotExist if not found

# Get or None
item = Item.objects.filter(id=1).first()  # Returns None if not found
```

### Create Objects

```python
from htk.apps.prelaunch.models.models import Item

# Create and save
item = Item.objects.create(
    name='test',
    description='...'
)

# Create instance, modify, then save
item = Item(name='test')
item.save()

# Bulk create
items = Item.objects.bulk_create([
    Item(name='item1'),
    Item(name='item2'),
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
class Item(models.Model):
    name = models.CharField(
        max_length=100,
        help_text='Item name',
        unique=True
    )

    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
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

Computed property:

```python
class Item(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
```

## Querysets

### Filtering

```python
# Exact match
Item.objects.filter(status='active')

# Greater than
Item.objects.filter(created__gt=datetime.now())

# Contains
Item.objects.filter(name__icontains='test')

# In list
Item.objects.filter(status__in=['active', 'pending'])
```

### Ordering

```python
# Ascending
Item.objects.all().order_by('name')

# Descending
Item.objects.all().order_by('-created')
```

## Best Practices

1. **Use QuerySets** - Dont fetch unnecessary data
2. **Select related** - Use `select_related()` for ForeignKey
3. **Prefetch related** - Use `prefetch_related()` for ManyToMany
4. **Index fields** - Add `db_index=True` to frequently filtered fields
5. **Use choices** - For fields with limited values
6. **Document fields** - Use `help_text`
7. **Add Meta class** - Configure ordering, permissions, verbose names
