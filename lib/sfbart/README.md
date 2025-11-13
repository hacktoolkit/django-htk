# SFBART Integration

San Francisco Bay Area Rapid Transit schedule and information.

## Quick Start

```python
from htk.lib.sfbart.api import make_api_request, get_schedule_arrive

# Get BART schedule
schedule = get_schedule_arrive(orig='EMBR', dest='CIVC')
```

## Configuration

```python
# settings.py
SFBART_API_KEY = os.environ.get('SFBART_API_KEY')
```

## Related Modules

- `htk.apps.geolocations` - Transit information
