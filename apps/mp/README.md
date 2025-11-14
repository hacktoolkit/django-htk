# MP App (Materialized Properties)

Performance optimization through materialized properties (computed fields stored in DB).

## Quick Start

```python
from htk.apps.mp.services import materialized_property, to_field_name, invalidate_for_instance

# Define materialized property on model
class User(models.Model):
    name = CharField(max_length=100)
    followers = ManyToManyField('self')

    # Materialized property field
    materialized_follower_count = IntegerField(default=0)

    @materialized_property
    def follower_count(self):
        """Expensive computation - materialized for O(1) access"""
        return self.followers.count()

# Access property (uses cached value)
user.materialized_follower_count  # O(1) lookup

# Invalidate when followers change
invalidate_for_instance(user, 'follower_count')
```

## Concept

Instead of computing expensive properties every time (O(n) or database queries), materialize them by:
1. Defining a `materialized_*` database field to store the value
2. Creating a `@materialized_property` method with the computation logic
3. Invalidating when dependencies change
4. Periodically recalculating in background jobs

**Benefits:**
- O(1) lookups instead of expensive queries
- Fast sorting/filtering on computed values
- Reduced database load
- Better performance at scale

**Trade-offs:**
- Extra database field
- Stale data (until invalidated)
- Need invalidation logic
- Background job to recalculate

## Common Patterns

### Basic Materialized Property

```python
from htk.apps.mp.services import materialized_property, to_field_name

class Product(models.Model):
    name = CharField(max_length=200)
    reviews = ManyToManyField(Review)
    materialized_review_count = IntegerField(default=0)

    @materialized_property
    def review_count(self):
        """Number of reviews (cached in DB)"""
        return self.reviews.count()

# Get field name for query
field_name = to_field_name('review_count')  # 'materialized_review_count'

# Sort by materialized property
products = Product.objects.order_by('-materialized_review_count')

# Filter by materialized property
popular = Product.objects.filter(materialized_review_count__gte=10)
```

### Aggregation Properties

```python
from django.db.models import Avg, Sum
from htk.apps.mp.services import materialized_property

class Product(models.Model):
    name = CharField(max_length=200)
    reviews = ManyToManyField(Review, through='ProductReview')

    materialized_avg_rating = DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0
    )
    materialized_total_sales = DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0
    )

    @materialized_property
    def avg_rating(self):
        """Average rating from reviews"""
        result = self.reviews.aggregate(
            avg=Avg('rating')
        )
        return result['avg'] or 0.0

    @materialized_property
    def total_sales(self):
        """Sum of all sales"""
        from django.db.models import Sum
        result = Order.objects.filter(
            product=self
        ).aggregate(total=Sum('amount'))
        return result['total'] or 0.0
```

### Invalidation on Signal

```python
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from htk.apps.mp.services import invalidate_for_instance

@receiver(post_save, sender=Review)
def invalidate_product_on_review(sender, instance, created, **kwargs):
    if created:
        # Invalidate when new review added
        invalidate_for_instance(instance.product, 'avg_rating')

@receiver(m2m_changed, sender=Product.followers.through)
def invalidate_follower_count(sender, instance, **kwargs):
    # Invalidate when followers change
    invalidate_for_instance(instance, 'follower_count')
```

### Batch Recalculation

```python
from celery import shared_task
from django.core.management.base import BaseCommand

@shared_task
def recalculate_materialized_properties():
    """Background task to recalculate all materialized properties"""

    # Recalculate all products
    for product in Product.objects.all():
        product.materialized_avg_rating = product.avg_rating
        product.materialized_total_sales = product.total_sales
        product.save()

# Or in management command
class Command(BaseCommand):
    def handle(self, *args, **options):
        recalculate_materialized_properties()
```

### Scheduled Updates

```python
from celery.schedules import crontab
from celery import shared_task

# Recalculate every hour
@shared_task
def hourly_sync_materialized():
    """Run every hour via Celery Beat"""
    from django.db.models import F, Count

    # Get items that changed recently
    User.objects.filter(
        updated__gte=timezone.now() - timedelta(hours=1)
    ).update(
        materialized_follower_count=Count('followers')
    )
```

## Performance Comparison

```python
# Without materialization - O(n) or complex query every access
product.reviews.count()  # Executes COUNT query

# With materialization - O(1) lookup
product.materialized_review_count  # Direct field access

# Sorting
# Without: Product.objects.annotate(review_count=Count('reviews')).order_by('-review_count')
# With: Product.objects.order_by('-materialized_review_count')  # Faster!
```

## Best Practices

1. **Use for expensive computations** - Only materialize costly queries
2. **Update on changes** - Invalidate when dependencies change
3. **Schedule batch updates** - Recalculate in background jobs
4. **Index materialized fields** - Add database index for fast filtering
5. **Document invalidation** - Clearly mark what invalidates each property
6. **Stale data tolerance** - Accept data may be stale between invalidations
7. **Monitor accuracy** - Verify materialized values match actual computed values

## Multiple Invalidations

```python
from htk.apps.mp.services import invalidate_for_instance

# Invalidate multiple properties at once
invalidate_for_instance(user, ['follower_count', 'post_count', 'like_count'])
```
