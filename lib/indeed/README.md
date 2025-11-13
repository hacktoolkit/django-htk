# Indeed Integration

Job posting and application tracking.

## Quick Start

```python
from htk.lib.indeed.api import IndeedJobSyncAPI, IndeedDispositionSyncAPI

job_api = IndeedJobSyncAPI()
disposition_api = IndeedDispositionSyncAPI()

# Sync job
job_data = {'title': 'Software Engineer', 'description': '...'}
job_api.create_job(job_data)

# Update application status
disposition_api.post_disposition(applicant_id, 'hired')
```

## Operations

```python
from htk.lib.indeed.api import get_access_token, generate_access_token

# Token management
token = get_access_token()
new_token = generate_access_token()

# Job operations
job_api.update_job(job_id, updated_data)
job_api.delete_job(job_id)
```

## Configuration

```python
# settings.py
INDEED_CLIENT_ID = os.environ.get('INDEED_CLIENT_ID')
INDEED_CLIENT_SECRET = os.environ.get('INDEED_CLIENT_SECRET')
```

## Related Modules

- `htk.apps.customers` - Candidate/applicant profiles
