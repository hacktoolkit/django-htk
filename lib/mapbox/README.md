# Mapbox Integration

Geocoding, reverse geocoding, and mapping.

## Quick Start

```python
from htk.lib.mapbox.geocode import reverse_geocode, reverse_geocode_with_context

# Reverse geocode latitude/longitude to address
address = reverse_geocode(lat=40.7128, lon=-74.0060)

# Reverse geocode with context (city, state, country)
location = reverse_geocode_with_context(lat=40.7128, lon=-74.0060)
```

## Configuration

```python
# settings.py
MAPBOX_ACCESS_TOKEN = os.environ.get('MAPBOX_ACCESS_TOKEN')
```

## Related Modules

- `htk.lib.geoip` - IP geolocation
- `htk.apps.geolocations` - Location-based features
- `htk.lib.google` - Maps API
