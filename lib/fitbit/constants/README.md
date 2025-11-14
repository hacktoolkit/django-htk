# Fitbit API Constants

API endpoints and resources for Fitbit API integration.

## Constants

```python
from htk.lib.fitbit.constants import FITBIT_API_BASE_URL, FITBIT_API_RESOURCES
```

## API Base URL

```python
FITBIT_API_BASE_URL = 'https://api.fitbit.com'
```

## API Resources

Dictionary mapping resource types to endpoint paths:

```python
FITBIT_API_RESOURCES = {
    # OAuth
    'refresh': '/oauth2/token',
    'revoke': '/oauth2/revoke',

    # Activity
    'activity-steps': lambda date, period: f'/1/user/-/activities/steps/date/{date}/{period}.json',

    # Body & Weight
    'fat': lambda date: f'/1/user/-/body/log/fat/date/{date}.json',
    'weight': lambda date: f'/1/user/-/body/log/weight/date/{date}.json',

    # Settings
    'devices': '/1/user/-/devices.json',
}
```

## Usage Example

```python
from htk.lib.fitbit.constants import FITBIT_API_BASE_URL, FITBIT_API_RESOURCES

# Build activity steps URL
date = '2023-10-15'
period = '1w'
endpoint = FITBIT_API_RESOURCES['activity-steps'](date, period)
url = f'{FITBIT_API_BASE_URL}{endpoint}'
```
