# HTK Models Module

> Django model base classes, custom fields (ULID, star ratings, ranges), and utilities.

## Purpose

The models module provides Django model extensions: base model classes with built-in caching and timestamps, specialized custom fields (ULID, StarRating, IntegerRange, CrossDBForeignKey), and utilities for common model operations.

## Quick Start

```python
from django.db import models
from htk.models.classes import HtkBaseModel
from htk.models.fields.ulid import ULIDField
from htk.models.fields.star_rating import StarRatingField

class Article(HtkBaseModel):
    """Article with HTK features"""
    title = models.CharField(max_length=255)
    content = models.TextField()
    # Includes: ULID id, created_at, updated_at, caching, JSON support

class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    rating = StarRatingField()  # 1-5 stars with validation
    comment = models.TextField()
```

## Key Components

| Component | Purpose |
|-----------|---------|
| **HtkBaseModel** | Abstract base with ULID id, timestamps, caching, JSON support |
| **ULIDField** | Sortable, efficient primary keys (vs UUID) |
| **StarRatingField** | Star ratings (1-5) with validation |
| **IntegerRangeField** | Integer ranges with min/max validation |
| **CrossDBForeignKeyField** | Foreign keys across databases |
| **FK Utilities** | `get_fk_field()`, `get_fk_queryset()` |

## Common Patterns

### Custom Fields

```python
from htk.models.fields.integer_range import IntegerRangeField
from htk.models.fields.cross_db_foreign_key import CrossDBForeignKeyField

class Product(models.Model):
    # ULID primary key (automatic with HtkBaseModel)
    id = ULIDField(primary_key=True)
    name = models.CharField(max_length=255)
    # Price range with validation
    price_range = IntegerRangeField(min_value=0, max_value=10000)

class Analytics(models.Model):
    # Reference user from different database
    user_id = CrossDBForeignKeyField(
        'auth.User',
        on_delete=models.CASCADE,
        db='analytics'
    )
```

### Foreign Key Utilities

```python
from htk.models.fk_fields import get_fk_field, get_fk_queryset

class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

# Get FK field descriptor and queryset
fk_field = get_fk_field(BlogPost, 'author')
authors = get_fk_queryset(BlogPost, 'author')
```

### Abstract Base Models

```python
class BaseEntity(HtkBaseModel):
    """Abstract base for all entities"""
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Document(BaseEntity):
    title = models.CharField(max_length=255)
    content = models.TextField()
```

### Model with Audit Trail

```python
class AuditableModel(HtkBaseModel):
    """Auditable model with timestamps"""
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # created_at and updated_at from HtkBaseModel

    class Meta:
        abstract = True
```

## Field Reference

| Field | Purpose | Example |
|-------|---------|---------|
| **ULIDField** | Sortable primary key | `id = ULIDField(primary_key=True)` |
| **StarRatingField** | 1-5 star ratings | `rating = StarRatingField()` |
| **IntegerRangeField** | Min/max ranges | `range = IntegerRangeField(min_value=0, max_value=100)` |
| **CrossDBForeignKeyField** | Cross-database FK | `user_id = CrossDBForeignKeyField('auth.User', db='other')` |

## Best Practices

- **Inherit from HtkBaseModel** - Get ULID id, timestamps, caching, JSON support automatically
- **Use ULIDField for primary keys** - Better than UUID for database indexing and sorting
- **Use specialized fields** - StarRatingField for ratings, IntegerRangeField for ranges
- **Validate at model level** - Call `full_clean()` before `save()`
- **Consider on_delete carefully** - Use CASCADE, SET_NULL, or SET_DEFAULT appropriately

## Testing

```python
from django.test import TestCase
from django.core.exceptions import ValidationError
from myapp.models import Product, Review

class ModelTestCase(TestCase):
    def test_product_creation(self):
        """Test product with custom fields."""
        product = Product.objects.create(
            name='Widget',
            price_range=(100, 500),
        )
        self.assertEqual(product.price_range, (100, 500))

    def test_review_rating_validation(self):
        """Test star rating field validation."""
        review = Review(rating=6)  # Invalid
        with self.assertRaises(ValidationError):
            review.full_clean()
```

## Related Modules

- `htk.models.classes` - Base model classes
- `htk.models.fields` - Custom model fields
- `htk.cache` - Model caching integration
- `htk.validators` - Field validators
- `htk.utils.django_shortcuts` - `get_object_or_none()` helper

## References

- [Django Models Documentation](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Model Fields](https://docs.djangoproject.com/en/stable/ref/models/fields/)
- [ULID Specification](https://github.com/ulid/spec)

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
