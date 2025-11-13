# Extensions

## Overview

The `extensions` module provides:

- Ordered sets with O(1) operations
- Custom data structure implementations
- Performance-optimized collections

## OrderedSet

A set that maintains insertion order with O(1) operations:

```python
from htk.extensions.data_structures.ordered_set import OrderedSet

# Create ordered set
tags = OrderedSet(['python', 'django', 'web', 'python'])
# OrderedSet(['python', 'django', 'web'])  # Duplicates removed, order preserved

# All set operations work
tags.add('api')
tags.remove('web')

# Maintains order
list(tags)  # ['python', 'django', 'api']

# Check membership in O(1)
'django' in tags  # True
```

**vs Python dict:**
```python
# OrderedSet is like an ordered set
tags = OrderedSet(['a', 'b', 'c'])

# vs dict (Python 3.7+)
tags_dict = dict.fromkeys(['a', 'b', 'c'])

# Functionally similar, but OrderedSet is optimized for set operations
```

## Use Cases

### Tracking Unique Items

```python
from htk.extensions.data_structures.ordered_set import OrderedSet

# Track user's visited pages (maintaining order)
visited = OrderedSet()
visited.add('/home')
visited.add('/products')
visited.add('/home')  # Won't be added again
visited.add('/checkout')

# Show visit history
breadcrumbs = list(visited)  # ['/home', '/products', '/checkout']
```

### Removing Duplicates While Preserving Order

```python
from htk.extensions.data_structures.ordered_set import OrderedSet

# Clean list while preserving order
tags = ['python', 'web', 'python', 'django', 'web', 'rest']
unique_tags = OrderedSet(tags)

list(unique_tags)  # ['python', 'web', 'django', 'rest']
```

### Set Operations

```python
from htk.extensions.data_structures.ordered_set import OrderedSet

set_a = OrderedSet(['a', 'b', 'c'])
set_b = OrderedSet(['b', 'c', 'd'])

# Union
union = set_a | set_b  # OrderedSet(['a', 'b', 'c', 'd'])

# Intersection
common = set_a & set_b  # OrderedSet(['b', 'c'])

# Difference
only_in_a = set_a - set_b  # OrderedSet(['a'])
```

## Performance Characteristics

| Operation | Time | Space |
|-----------|------|-------|
| Add | O(1) | O(n) |
| Remove | O(1) | O(n) |
| Contains | O(1) | |
| Iterate | O(n) | |
| Union | O(n+m) | O(n+m) |
| Intersection | O(min(n,m)) | |

## Alternatives

- **Python set**: Fast but unordered
- **Python list**: Ordered but slow membership tests
- **OrderedSet**: Ordered AND fast membership tests

## Best Practices

1. **Use when you need both ordering and uniqueness**
2. **Don't use if order doesn't matter** - use `set()` instead
3. **Don't use for very large datasets** - memory overhead
4. **Use for deduplication** - clean lists while preserving order

## Common Patterns

### Merge Multiple Lists

```python
from htk.extensions.data_structures.ordered_set import OrderedSet

list1 = [1, 2, 3]
list2 = [2, 3, 4]
list3 = [3, 4, 5]

merged = OrderedSet()
merged.update(list1)
merged.update(list2)
merged.update(list3)

result = list(merged)  # [1, 2, 3, 4, 5]
```

### Unique Query Results

```python
from django.db.models import Q
from htk.extensions.data_structures.ordered_set import OrderedSet

# Get unique users from multiple queries
query1 = User.objects.filter(country='US')
query2 = User.objects.filter(premium=True)
query3 = User.objects.filter(created__year=2024)

all_users = OrderedSet()
all_users.update(query1)
all_users.update(query2)
all_users.update(query3)

# Avoid duplicates without complex Q queries
```
