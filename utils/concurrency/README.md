# Concurrency Utilities

Race condition resolution and retry patterns.

## Quick Start

```python
from htk.utils.concurrency.race_resolvers import retry_until_not_none, retry_until

# Retry until function returns non-None value
result = retry_until_not_none(lambda: get_data(), timeout=10)

# Retry until predicate is true
result = retry_until(
    lambda: fetch_status(),
    until_predicate=lambda x: x == 'completed',
    timeout=30
)
```

## Common Patterns

```python
# Waiting for async operations
def wait_for_resource():
    return retry_until_not_none(
        lambda: get_resource(),
        timeout=60,
        retry_delay=0.1
    )
```

## Related Modules

- `htk.apps.async_task` - Asynchronous tasks
- `htk.lib.rabbitmq` - Message queues
