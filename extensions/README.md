# HTK Extensions Module

> Extended data structures and Python language extensions.

## Purpose

The extensions module provides extended implementations of Python's built-in data structures that combine performance with behavior needed in web applications. OrderedSet maintains insertion order while providing O(1) lookup and deduplication.

## Quick Start

```python
from htk.extensions.data_structures import OrderedSet

# Create from list (duplicates removed, order preserved)
tags = OrderedSet(['python', 'django', 'web', 'django', 'python'])
print(list(tags))  # ['python', 'django', 'web']

# Add items
tags.add('rest')
tags.add('python')  # Ignored, already present
print(list(tags))  # ['python', 'django', 'web', 'rest']

# Set operations
set1 = OrderedSet([1, 2, 3])
set2 = OrderedSet([3, 4, 5])

union = set1 | set2  # [1, 2, 3, 4, 5]
intersection = set1 & set2  # [3]
difference = set1 - set2  # [1, 2]
```

## Key Features

**OrderedSet:**
- **Preserves order** - Maintains insertion order like a list
- **Fast lookup** - O(1) membership testing like a set
- **Deduplication** - Automatically removes duplicates
- **Set operations** - Supports union, intersection, difference
- **Hashable items only** - Items must be hashable

## Common Patterns

### Deduplication While Preserving Order

```python
from htk.extensions.data_structures import OrderedSet

def get_unique_tags(posts):
    """Get unique tags in order they were added"""
    tags = OrderedSet()
    for post in posts:
        for tag in post.tags.all():
            tags.add(tag)
    return list(tags)

# Example
posts = [...]
unique_tags = get_unique_tags(posts)
# Original: ['python', 'django', 'web', 'django', 'python', 'rest']
# Result: ['python', 'django', 'web', 'rest']
```

### Building Collections from Multiple Sources

```python
from htk.extensions.data_structures import OrderedSet

def merge_priority_lists(lists):
    """Merge lists, removing duplicates, preserving order"""
    result = OrderedSet()
    for item_list in lists:
        result.update(item_list)
    return list(result)

# Example
list1 = ['apple', 'banana', 'cherry']
list2 = ['banana', 'date', 'apple']
merged = merge_priority_lists([list1, list2])
# Result: ['apple', 'banana', 'cherry', 'date']
```

### Set Operations in Queries

```python
from django.db.models import Q
from htk.extensions.data_structures import OrderedSet

def find_items_in_all_categories(category_ids):
    """Find items common to multiple categories"""
    if not category_ids:
        return []

    category_items = [
        OrderedSet(Item.objects.filter(category_id=cat_id))
        for cat_id in category_ids
    ]

    # Intersection: items in all categories
    result = category_items[0]
    for items_set in category_items[1:]:
        result &= items_set

    return list(result)
```

## OrderedSet vs Alternatives

| Use Case | OrderedSet | List | Set | Dict |
|----------|-----------|------|-----|------|
| Fast lookup | ✓ O(1) | ✗ O(n) | ✓ O(1) | ✓ O(1) |
| Preserve order | ✓ | ✓ | ✗ | ✓ (3.7+) |
| Deduplication | ✓ | ✗ | ✓ | ✓ |
| Set operations | ✓ | ✗ | ✓ | ✗ |
| Hashable items | ✓ | ✓ | ✓ | ✓ (values) |

## Performance Characteristics

| Operation | Time Complexity |
|-----------|-----------------|
| Add, Remove, Contains, Pop | O(1) |
| Clear | O(n) |
| Iteration | O(n) |
| Union, Intersection, Difference | O(m+n) |

## When to Use OrderedSet

**Use when:**
- Fast membership testing needed
- Duplicates must be removed
- Insertion order must be preserved
- All items are hashable

**Don't use when:**
- Items need specific sort order (use `sorted()`)
- Items are not hashable (use list)
- Frequent slicing needed (use list)
- Negative indexing needed (use list)

## Best Practices

- **Initialize with data** - Pass iterable to constructor for efficiency
- **Use set operations** - Union/intersection/difference for combining collections
- **Check membership first** - Use `in` before modifying for clarity
- **Document requirements** - Be explicit that items must be hashable
- **Test edge cases** - Empty sets, single items, duplicates

## Testing

```python
from django.test import TestCase
from htk.extensions.data_structures import OrderedSet

class OrderedSetTestCase(TestCase):
    def test_deduplication_and_order(self):
        """OrderedSet removes duplicates while preserving order"""
        items = OrderedSet([1, 2, 3, 2, 1])
        self.assertEqual(list(items), [1, 2, 3])

    def test_set_operations(self):
        """OrderedSet supports standard set operations"""
        set1 = OrderedSet([1, 2, 3])
        set2 = OrderedSet([3, 4, 5])

        self.assertEqual(list(set1 | set2), [1, 2, 3, 4, 5])  # Union
        self.assertEqual(list(set1 & set2), [3])  # Intersection
        self.assertEqual(list(set1 - set2), [1, 2])  # Difference

    def test_add_and_remove(self):
        """OrderedSet add/remove operations"""
        items = OrderedSet([1, 2, 3])
        items.add(4)
        items.remove(2)
        self.assertEqual(list(items), [1, 3, 4])
```

## Related Modules

- `htk.extensions.data_structures` - Data structure implementations
- `htk.utils.data_structures` - Data structure utilities

## References

- [Python Sets Documentation](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
- [Collections.OrderedDict](https://docs.python.org/3/library/collections.html#collections.OrderedDict)

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
