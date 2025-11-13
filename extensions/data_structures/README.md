# Data Structures

Extended data structures with optimized performance characteristics.

## Quick Start

```python
from htk.extensions.data_structures import OrderedSet

# Create ordered set (maintains insertion order + uniqueness)
tags = OrderedSet(['python', 'django', 'web', 'python'])
# Result: OrderedSet(['python', 'django', 'web'])

# All set operations
tags.add('api')
tags.remove('web')

# Check membership in O(1)
'django' in tags  # True
list(tags)  # ['python', 'django', 'api']
```

## OrderedSet

A set that maintains insertion order with O(1) operations for all standard set operations.

### Features

```python
from htk.extensions.data_structures import OrderedSet

# Create from list (removes duplicates, preserves order)
items = OrderedSet([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])
print(list(items))  # [3, 1, 4, 5, 9, 2, 6]

# Add items
items.add(7)
items.add(3)  # No duplicate (already exists)

# Remove items
items.discard(4)  # Won't raise if not found
items.remove(5)   # Raises KeyError if not found

# Set operations
set_a = OrderedSet(['a', 'b', 'c'])
set_b = OrderedSet(['b', 'c', 'd'])

union = set_a | set_b           # OrderedSet(['a', 'b', 'c', 'd'])
intersection = set_a & set_b    # OrderedSet(['b', 'c'])
difference = set_a - set_b      # OrderedSet(['a'])

# Iterate in order
for item in items:
    print(item)

# Check membership
'a' in set_a  # O(1) lookup time
```

### Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Add | O(1) | Append to list + add to set |
| Remove | O(n) | Delete from list is O(n) |
| Contains (`in`) | O(1) | Set lookup |
| Iteration | O(n) | Maintains insertion order |
| Union | O(n+m) | Merge two ordered sets |
| Intersection | O(min(n,m)) | Common elements |

### Common Patterns

#### Deduplication While Preserving Order

```python
from htk.extensions.data_structures import OrderedSet

# Remove duplicates from list
results = [5, 2, 8, 2, 5, 1, 8, 3]
unique = OrderedSet(results)
print(list(unique))  # [5, 2, 8, 1, 3]

# vs Python set (order lost)
print(set(results))  # {1, 2, 3, 5, 8} - unordered
```

#### Track User Interactions

```python
from htk.extensions.data_structures import OrderedSet

class UserSession:
    def __init__(self, user):
        self.user = user
        self.visited_pages = OrderedSet()

    def visit_page(self, page_url):
        self.visited_pages.add(page_url)

    def get_breadcrumbs(self):
        return list(self.visited_pages)

# Usage
session = UserSession(user)
session.visit_page('/home')
session.visit_page('/products')
session.visit_page('/home')  # Won't duplicate
session.visit_page('/checkout')

breadcrumbs = session.get_breadcrumbs()
# ['/home', '/products', '/checkout']
```

#### Merge Multiple Lists

```python
from htk.extensions.data_structures import OrderedSet

# Combine multiple lists without duplicates
recommended = [1, 2, 3, 4, 5]
wishlist = [3, 4, 5, 6, 7]
trending = [5, 8, 9]

merged = OrderedSet()
merged.update(recommended)
merged.update(wishlist)
merged.update(trending)

items = list(merged)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

#### Query Results Deduplication

```python
from htk.extensions.data_structures import OrderedSet
from django.db.models import Q

# Get unique items from multiple queries
recent_users = User.objects.filter(created__gte=today).order_by('-created')
premium_users = User.objects.filter(premium=True)
search_results = User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))

all_users = OrderedSet()
for user in recent_users:
    all_users.add(user)
for user in premium_users:
    all_users.add(user)
for user in search_results:
    all_users.add(user)

result_list = list(all_users)  # No duplicates, maintains order
```

## Use Cases

**Use OrderedSet when you need:**
- Uniqueness (no duplicates)
- Order preservation (insertion order)
- Fast membership testing (O(1) lookup)

**Don't use OrderedSet if:**
- Order doesn't matter → use `set()`
- You need fast removal → use `list` + `set` hybrid
- Very large datasets → memory overhead may be high

## Alternatives

| Structure | Order | Unique | Lookup | Notes |
|-----------|-------|--------|--------|-------|
| `set()` | ✗ | ✓ | O(1) | Fast, unordered |
| `list` | ✓ | ✗ | O(n) | Ordered, slow lookup |
| `dict.keys()` | ✓ | ✓ | O(1) | Python 3.7+, ordered |
| `OrderedSet` | ✓ | ✓ | O(1) | Best of both worlds |

## Best Practices

1. **Use for deduplication** - Clean lists while preserving order
2. **Avoid for large sets** - Memory overhead is 2x+ vs regular set
3. **Set operations are powerful** - Union, intersection, difference
4. **Don't rely on order across versions** - Implementation details may change

## Related Modules

- `htk.utils.data_structures` - More data structure utilities
- `collections` - Python's built-in data structures
- `collections.OrderedDict` - Similar for key-value pairs
