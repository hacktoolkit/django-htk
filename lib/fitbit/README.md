# Fitbit Integration

Fitness tracking, activity, and health data.

## Quick Start

```python
from htk.lib.fitbit.api import FitbitAPI

api = FitbitAPI()

# Get activity data
steps = api.get_activity_steps_for_period(start_date, end_date)
weight_logs = api.get_weight_logs('2024-01-01')
body_fat = api.get_body_fat_logs('2024-01-01')

# List devices
devices = api.get_devices()
```

## Operations

```python
# Get historical activity
steps_past_month = api.get_activity_steps_past_month()
steps_past_year = api.get_activity_steps_past_year()

# Custom API requests
api.post('/resource', data={'key': 'value'})
api.get('/resource')
```

## Configuration

```python
# settings.py
FITBIT_CLIENT_ID = os.environ.get('FITBIT_CLIENT_ID')
FITBIT_CLIENT_SECRET = os.environ.get('FITBIT_CLIENT_SECRET')
FITBIT_ACCESS_TOKEN = os.environ.get('FITBIT_ACCESS_TOKEN')
```
