# LinkedIn Integration

Professional networking and recruitment API.

## Quick Start

```python
from htk.lib.linkedin import Client

client = Client(api_key='your_api_key')
result = client.get_data()
```

## Configuration

```python
# settings.py
LINKEDIN_CLIENT_ID = os.environ.get('LINKEDIN_CLIENT_ID')
LINKEDIN_CLIENT_SECRET = os.environ.get('LINKEDIN_CLIENT_SECRET')
```

## Related Modules

- `htk.apps.accounts` - Social auth
- `htk.lib.facebook` - OAuth patterns
- `htk.lib.glassdoor` - Recruitment
