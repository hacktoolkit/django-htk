# Scripts

## Quick Start

```python
from htk.scripts.utils import job_runner

# Define a job function
def update_user_stats():
    print("Updating user statistics...")
    for user in User.objects.all():
        user.update_stats()

# Run the job
job_runner(update_user_stats)
```

## Job Runner

Execute any callable function as a job:

```python
from htk.scripts.utils import job_runner

# Run simple function
def sync_external_data():
    # Long-running operation
    pass

job_runner(sync_external_data)

# Run with arguments
def process_user(user_id):
    user = User.objects.get(id=user_id)
    # Process user
    pass

job_runner(lambda: process_user(123))
```

## Management Commands

Use with Django management commands:

```python
from django.core.management.base import BaseCommand
from htk.scripts.utils import job_runner

class Command(BaseCommand):
    def handle(self, *args, **options):
        job_runner(self.sync_data)

    def sync_data(self):
        # Sync logic
        pass
```

## Testing Scripts

```python
# Scripts are tested in tests.py
from django.test import TestCase
from htk.scripts.utils import job_runner

class ScriptTestCase(TestCase):
    def test_job_runner(self):
        # Job should complete successfully
        job_runner(lambda: print("test"))
```

## Common Patterns

### Batch Processing

```python
from htk.scripts.utils import job_runner

def batch_process_orders():
    orders = Order.objects.filter(status='pending')
    for order in orders:
        order.process()
        order.save()

job_runner(batch_process_orders)
```

### Scheduled Tasks

```python
# With Celery or APScheduler
from htk.scripts.utils import job_runner

def scheduled_sync():
    job_runner(sync_external_api)
```
