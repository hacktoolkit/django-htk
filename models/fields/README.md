# Custom Model Fields

Django model field types for common patterns and advanced use cases.

## Quick Start

```python
from htk.models.fields import ULIDField, CrossDBForeignKey, StarRatingField, IntegerRangeField

class Product(models.Model):
    id = ULIDField(primary_key=True)
    name = models.CharField(max_length=200)
    rating = StarRatingField(default=0)
    price_range = IntegerRangeField(default=(0, 1000))

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    score = StarRatingField(min_value=1, max_value=5)
```

## ULIDField

Use ULIDs (Universally Unique Lexicographically Sortable Identifiers) as primary keys or unique identifiers.

**Advantages over UUID:**
- Sortable by timestamp
- URL-friendly (no hyphens)
- Case-insensitive
- Timestamp-encoded (creation time extractable)
- Shorter representation

```python
from htk.models.fields import ULIDField

class Article(models.Model):
    id = ULIDField(primary_key=True)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

# Usage
article = Article.objects.create(title='Test')
print(article.id)  # 01ARZ3NDEKTSV4RRFFQ69G5FAV

# ULIDs are sortable - newer IDs are greater
articles = Article.objects.all()  # Automatically ordered by ULID (creation time)
```

### ULID Structure

```
01ARZ3NDEKTSV4RRFFQ69G5FAV
││││││││││││││││││││││││││
│││││││││└────────────────┘ Randomness (80 bits)
└────────┘────────────────┘ Timestamp (48 bits = milliseconds since epoch)
```

### Use Cases

```python
from htk.models.fields import ULIDField
from datetime import datetime

# Sortable primary keys
class Event(models.Model):
    id = ULIDField(primary_key=True)
    name = models.CharField(max_length=100)

# Events are automatically ordered chronologically
recent_events = Event.objects.order_by('-id')  # Newest first

# Extract creation time from ULID
from ulid import ULID
event = Event.objects.first()
creation_time = ULID(str(event.id)).timestamp()
```

## CrossDBForeignKey

Create foreign key relationships across different databases (multi-database architectures).

**Use Cases:**
- Multi-database sharding
- Legacy data migrations
- Microservices integration
- Database split scenarios

```python
from htk.models.fields import CrossDBForeignKey

class Order(models.Model):
    # Reference User from different database
    user_id = CrossDBForeignKey(
        User,
        on_delete=models.CASCADE,
        db_constraint=False  # No database constraint across databases
    )
    order_number = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def get_user(self):
        # Manual lookup across databases
        return User.objects.using('users_db').get(id=self.user_id)
```

### Multi-Database Setup

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'orders_db',
    },
    'users_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'users_db',
    }
}

# Usage
class Order(models.Model):
    user_id = CrossDBForeignKey(User, on_delete=models.CASCADE, db_constraint=False)

# Queries must specify database
user = User.objects.using('users_db').get(id=order.user_id)
```

## StarRatingField

Store and validate star ratings (typically 1-5 stars or custom range).

```python
from htk.models.fields import StarRatingField

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = StarRatingField(
        min_value=1,
        max_value=5,
        default=0
    )
    comment = models.TextField()

# Usage
review = Review.objects.create(
    product=product,
    rating=4,
    comment='Great product!'
)

# Validates range (1-5)
review.rating = 6  # Will fail validation
review.full_clean()  # Raises ValidationError
```

### Common Patterns

```python
from django.db.models import Avg, Q
from htk.models.fields import StarRatingField

# Get average rating
average = Review.objects.filter(product=product).aggregate(
    avg_rating=Avg('rating')
)['avg_rating']

# Filter by rating range
highly_rated = Review.objects.filter(rating__gte=4)
poor_reviews = Review.objects.filter(rating__lt=3)

# Rating distribution
distribution = Review.objects.values('rating').annotate(
    count=Count('id')
).order_by('rating')
```

## IntegerRangeField

Store a range of integers (min/max pair) efficiently.

```python
from htk.models.fields import IntegerRangeField

class PriceListItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Store price range as a single field
    price_range = IntegerRangeField()

# Usage
item = PriceListItem.objects.create(
    product=product,
    price_range=(100, 500)  # (min, max)
)

print(item.price_range)  # (100, 500)
print(item.price_range[0])  # 100 (min)
print(item.price_range[1])  # 500 (max)
```

### Query Ranges

```python
from htk.models.fields import IntegerRangeField

# Find items where price is in range
class Inventory(models.Model):
    quantity_range = IntegerRangeField()

# Get inventory with stock between 10-100
low_stock = Inventory.objects.filter(
    quantity_range__gte=(10, 100)
)
```

## Best Practices

1. **ULIDField** - Use for sortable primary keys
2. **CrossDBForeignKey** - Only use in multi-database architectures
3. **StarRatingField** - Validate range in model clean() method
4. **IntegerRangeField** - Use for efficient min/max storage

## Common Patterns

### Validating Custom Fields

```python
from django.core.exceptions import ValidationError

class Article(models.Model):
    id = ULIDField(primary_key=True)
    rating = StarRatingField(min_value=1, max_value=5)
    word_count_range = IntegerRangeField()

    def clean(self):
        super().clean()
        # Validate rating
        if not (1 <= self.rating <= 5):
            raise ValidationError({'rating': 'Rating must be 1-5'})

        # Validate range
        min_words, max_words = self.word_count_range
        if min_words >= max_words:
            raise ValidationError({'word_count_range': 'Min must be less than max'})
```

### Database Query Examples

```python
from django.db.models import Avg, Count, Q
from htk.models.fields import ULIDField, StarRatingField

# Get trending items (high rating + recent ULID)
trending = Product.objects.annotate(
    avg_rating=Avg('review__rating')
).filter(
    avg_rating__gte=4,
    id__gte=threshold_ulid  # Recent ULIDs
).order_by('-id')

# Rating distribution
distribution = Review.objects.values('rating').annotate(
    count=Count('id'),
    percentage=Count('id') * 100.0 / Count('*')
).order_by('-rating')
```
