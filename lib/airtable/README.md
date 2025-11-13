# Airtable Integration

Spreadsheet-like database API.

## Quick Start

```python
from htk.lib.airtable.api import AirtableAPI

api = AirtableAPI()
records = api.fetch_records('table_name')

for record in records:
    print(record['id'], record['fields'])
```

## Configuration

```python
# settings.py
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
```

## Related Modules

- `htk.apps.kv_storage` - Alternative data storage
