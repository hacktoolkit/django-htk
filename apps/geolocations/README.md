# Geolocations App

Geolocation and proximity search.

## Quick Start

```python
from htk.apps.geolocations.models import AbstractGeolocation
from htk.apps.geolocations.utils import get_latlng, haversine

# Create location
location = AbstractGeolocation.objects.create(
    name='San Francisco HQ',
    address='123 Market St, San Francisco, CA'
)

# Geocode (get lat/lng)
location.geocode()  # Populates latitude, longitude

# Get latlng from address
lat, lng = get_latlng('New York, NY')

# Find nearby locations
nearby = AbstractGeolocation.find_near_latlng(
    lat=37.7749,
    lng=-122.4194,
    distance=10  # miles
)

# Calculate distance
distance = location.distance_from(37.7749, -122.4194)
```

## Models

- **`AbstractGeolocation`** - Location with lat/lng

## Utilities

```python
# Convert distance units
from htk.apps.geolocations.utils import convert_distance_to_meters, convert_meters

meters = convert_distance_to_meters(10, 'miles')
km = convert_meters(1000, 'km')

# Get bounding box
from htk.apps.geolocations.utils import get_bounding_box

bbox = get_bounding_box(lat=37.7749, lng=-122.4194, radius=5)

# WGS84 Earth radius
from htk.apps.geolocations.utils import WGS84EarthRadius

radius = WGS84EarthRadius(lat=37.7749)
```

## Configuration

```python
# settings.py
GEOLOCATIONS_CACHE_TTL = 86400  # 1 day
GEOLOCATIONS_DEFAULT_DISTANCE_UNIT = 'miles'
```

## Related Modules

- `htk.apps.addresses` - Address management
- `htk.lib.google.geocode` - Google Geocoding
- `htk.lib.mapbox` - Mapbox integration
