# MP App (Materialized Properties)

Performance optimization through materialized properties.

## Quick Start

```python
from htk.apps.mp.services import materialized_property, to_field_name

# Define materialized property
class User(models.Model):
    name = CharField(max_length=100)

    @materialized_property
    def follower_count(self):
        return self.followers.count()

# Access property
user.materialized_follower_count  # Stored in DB field

# Invalidate when data changes
from htk.apps.mp.services import invalidate_for_instance
invalidate_for_instance(user, 'follower_count')
```

## Concept

Instead of computing properties on every access, materialize (store) them in the database for O(1) lookups.

## Common Patterns

```python
# Get materialized field name
field_name = to_field_name('follower_count')  # Returns 'materialized_follower_count'

# Invalidate multiple properties
invalidate_for_instance(user, ['follower_count', 'post_count'])
```

## Best Practices

1. **Use for expensive computations** - Queries that take time
2. **Update on related changes** - Invalidate when dependencies change
3. **Schedule batch updates** - Recalculate in background jobs
4. **Index materialized fields** - For fast sorting/filtering

## Related Modules

- `htk.cache` - For alternative caching approach
