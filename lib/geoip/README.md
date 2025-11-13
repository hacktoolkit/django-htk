# GeoIP Integration

IP geolocation and city/country lookup.

## Quick Start

```python
from htk.lib.geoip.utils import get_record_by_ip, get_country_code_by_ip, get_timezone_by_ip

# Get full geolocation record
record = get_record_by_ip('8.8.8.8')
# Returns: country_code, country_name, region, city, postal_code, latitude, longitude, timezone

# Get specific values
country = get_country_code_by_ip('8.8.8.8')
timezone = get_timezone_by_ip('8.8.8.8')
```

## Configuration

```python
# settings.py
GEOIP_API_KEY = os.environ.get('GEOIP_API_KEY')
```

## Related Modules

- `htk.apps.geolocations` - Location-based features
- `htk.lib.mapbox` - Geocoding and mapping
