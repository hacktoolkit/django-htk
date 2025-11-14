# Async Task App

Asynchronous background task execution and result tracking.

## Quick Start

```python
from htk.apps.async_task.models import AsyncTask

# Create async task
task = AsyncTask.objects.create(
    task_name='generate_report',
    status='pending'
)

# Execute task
task.execute()  # Run in background

# Check status
task.refresh_from_db()
if task.status == 'completed':
    result = task.result
```

## Common Patterns

```python
# Build result from JSON
from htk.apps.async_task.utils import build_async_task_result

result = build_async_task_result(
    task,
    data={'report_id': 123, 'url': '/reports/123/'}
)

# Extract result values
from htk.apps.async_task.utils import extract_async_task_result_json_values

values = extract_async_task_result_json_values(task)
```

## Views

```python
# Download task result
from htk.apps.async_task.views import async_download_result
# GET /async-task/123/download/
```

## Configuration

```python
# settings.py
ASYNC_TASK_TIMEOUT = 3600  # 1 hour
ASYNC_TASK_MAX_RETRIES = 3
```
