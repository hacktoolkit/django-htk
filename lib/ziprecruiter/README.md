# ZipRecruiter Integration

Job posting and recruitment API.

## Quick Start

```python
from htk.lib.ziprecruiter.api import ZipRecruiterAPI

api = ZipRecruiterAPI()

# Create job
job = api.create_job({
    'title': 'Software Engineer',
    'description': 'Job description...',
    'location': 'San Francisco, CA'
})

# Update job
api.update_job(job_id, {'title': 'Senior Software Engineer'})

# Delete job
api.delete_job(job_id)
```

## Configuration

```python
# settings.py
ZIPRECRUITER_API_KEY = os.environ.get('ZIPRECRUITER_API_KEY')
```

## Related Modules

- `htk.apps.customers` - Candidate management
- `htk.lib.indeed` - Job posting integration
