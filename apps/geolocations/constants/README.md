# Geolocations Constants

## Overview

This module provides geolocation constants for location searches, distance conversions, and WGS-84 geodetic reference parameters.

## Constants

### Mapbox Configuration

- **`HTK_GEOLOCATIONS_MAPBOX_MIN_RELEVANCE_THRESHOLD`** - Default: `1` - Minimum relevance score for Mapbox results

### Location Configuration

- **`LOCATION_MAP_URL_FORMAT`** - Google Maps URL template: `'https://maps.google.com/?q=%s'`
- **`DEFAULT_SEARCH_RADIUS`** - Default: `10` - Default search radius (in default distance unit)
- **`DEFAULT_DISTANCE_UNIT`** - Default: `DistanceUnit.MILE` - Default unit for distances

### Distance Conversions

- **`FEET_PER_MILE`** - `5280.0`
- **`KM_PER_MILE`** - `1.609344`
- **`METERS_PER_KM`** - `1000.0`
- **`MILES_PER_KM`** - `0.62137119`
- **`METERS_PER_MILE`** - Calculated: `1609.344`
- **`METERS_PER_FEET`** - Calculated: `0.3048`

### WGS-84 Reference Parameters

- **`WGS84_a`** - Major semiaxis: `6378137.0` meters
- **`WGS84_b`** - Minor semiaxis: `6356752.3142` meters

## Enums

### DistanceUnit

Units for distance measurements:

```python
from htk.apps.geolocations.enums import DistanceUnit

# Available units with values
DistanceUnit.MILE           # value: 1
DistanceUnit.KILOMETER      # value: 2
DistanceUnit.FEET           # value: 3
DistanceUnit.METER          # value: 4

# Access enum properties
unit = DistanceUnit.MILE
print(f"{unit.name}: {unit.value}")  # MILE: 1
```

## Usage Examples

### Convert Distances

```python
from htk.apps.geolocations.constants import (
    KM_PER_MILE, METERS_PER_KM, FEET_PER_MILE
)

miles = 5
km = miles * KM_PER_MILE
meters = km * METERS_PER_KM
feet = miles * FEET_PER_MILE
```

### Create Location Map URL

```python
from htk.apps.geolocations.constants import LOCATION_MAP_URL_FORMAT

location = "1600 Pennsylvania Avenue, Washington DC"
map_url = LOCATION_MAP_URL_FORMAT % location
```

### Configure Search Radius

```python
# In Django settings.py
from htk.apps.geolocations.enums import DistanceUnit

DEFAULT_SEARCH_RADIUS = 25  # 25 miles
DEFAULT_DISTANCE_UNIT = DistanceUnit.KILOMETER
```
