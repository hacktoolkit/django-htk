# Models & Fields

Abstract base models and custom field types for Django models.

## Overview

The `models` module provides:

- Abstract base model classes for common patterns
- Custom Django field types (ULID, Cross-DB Foreign Keys)
- JSON serialization helpers
- Model field utilities

## Base Models

### HtkBaseModel

Abstract base class extending Django's Model:

```python
from htk.models.classes import HtkBaseModel

class Article(HtkBaseModel):
    title = CharField(max_length=200)
    content = TextField()
    published = BooleanField(default=False)
```

**Inherited Features:**
- Timestamp fields (created, updated)
- UUID or ULID primary keys
- JSON serialization
- Consistent model behavior

## Custom Field Types

### ULIDField

Use ULIDs (Universally Unique Lexicographically Sortable Identifiers) instead of UUIDs:

```python
from htk.models.fields.ulid import ULIDField

class User(models.Model):
    id = ULIDField(primary_key=True)
    email = EmailField(unique=True)

# Usage
user = User.objects.create(email='user@example.com')
print(user.id)  # 01ARZ3NDEKTSV4RRFFQ69G5FAV
```

**Advantages over UUID:**
- Sortable (chronological ordering)
- Case-insensitive
- No hyphens (more URL-friendly)
- Timestamp-encoded (can determine creation time)

### CrossDBForeignKey

Create foreign keys across different databases:

```python
from htk.models.fields.cross_db_foreign_key import CrossDBForeignKey

class Order(models.Model):
    # Reference User from different database
    user_id = CrossDBForeignKey(User, on_delete=models.CASCADE)
```

**Use Cases:**
- Multi-database architectures
- Sharded databases
- Legacy data migrations

## Model Utilities

### JSON Serialization

```python
from htk.models.classes import HtkBaseModel

class Article(HtkBaseModel):
    title = CharField(max_length=200)
    author = CharField(max_length=100)

    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'author': self.author,
            'created': self.created.isoformat(),
        }

# Usage
article = Article.objects.first()
json_data = json.dumps(article.to_dict())
```

### Field Value Normalization

```python
from htk.models.utils import normalize_model_field_value

# Normalize value for a specific field
user = User.objects.first()
normalized = normalize_model_field_value(user, 'birth_date', '2000-01-15')
```

## Attribute Holder Pattern

Store arbitrary attributes on models without creating new fields:

```python
from htk.models.classes import AbstractAttribute, AbstractAttributeHolderClassFactory

# Create model for storing attributes
AttributeHolder = AbstractAttributeHolderClassFactory(User, 'user_id')

# Store attributes
attr = AttributeHolder.objects.create(
    user=user,
    key='preferences',
    value={'theme': 'dark', 'notifications': True}
)

# Retrieve attributes
prefs = AttributeHolder.objects.get(user=user, key='preferences').value
```

**Benefits:**
- Flexible schema without migrations
- No need for separate columns
- JSON storage support
- Indexable keys

## Common Patterns

### Custom Model with Timestamps

```python
from htk.models.classes import HtkBaseModel
from django.db import models

class BlogPost(HtkBaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']  # Newest first

# Inherited fields:
# - id: ULIDField (auto)
# - created: DateTimeField (auto)
# - updated: DateTimeField (auto)
```

### ULID Primary Keys

```python
from htk.models.fields.ulid import ULIDField

class Product(models.Model):
    id = ULIDField(primary_key=True)
    name = CharField(max_length=100)
    price = DecimalField(max_digits=10, decimal_places=2)

# Usage
product = Product.objects.create(
    name='Widget',
    price=19.99
)
# ID is automatically generated as ULID
```

### Model Composition

```python
from htk.models.classes import HtkBaseModel

class BaseContent(HtkBaseModel):
    title = CharField(max_length=200)
    body = TextField()
    author = ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True  # Allow inheritance

class Article(BaseContent):
    category = CharField(max_length=50)

class Page(BaseContent):
    slug = SlugField(unique=True)
```

## Best Practices

1. **Extend HtkBaseModel** for new models to get timestamps
2. **Use ULIDField** for sortable, URL-friendly IDs
3. **Use CrossDBForeignKey** only when necessary (multi-db)
4. **Use AttributeHolder** for flexible, schema-less data
5. **Normalize field values** before storage
6. **Override to_dict()** for JSON serialization

## Classes

- **`HtkBaseModel`** - Abstract base model with timestamps
- **`AbstractAttribute`** - Store key-value attributes on models
- **`AbstractAttributeHolderClassFactory`** - Factory for attribute holders
- **`ULID`** - ULID wrapper class with utilities
- **`ULIDField`** - Django field type for ULIDs
- **`CrossDBForeignKey`** - Foreign key across databases

## Functions

- **`json_encode`** - Serialize model instance to JSON-compatible dict
- **`json_decode`** - Deserialize JSON to model fields
- **`attribute_fields`** - Get list of attribute keys
- **`boolean_attributes_lookup`** - Find boolean-valued attributes
- **`normalize_model_field_value`** - Normalize value for field type
