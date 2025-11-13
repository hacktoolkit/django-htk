# Addresses App

Postal address management with geocoding support.

## Quick Start

```python
from htk.apps.addresses.models import BasePostalAddress

# Create address
address = BasePostalAddress.objects.create(
    street_1='123 Main St',
    city='San Francisco',
    state='CA',
    postal_code='94105',
    country='US'
)

# Get Google Maps static image
from htk.apps.addresses.mixins import get_static_google_map_image_url
map_url = get_static_google_map_image_url(address)
```

## Models

- **`BasePostalAddress`** - Postal address with geocoding

## Integration

```python
# Add address to user profile
class UserProfile(BaseAbstractUserProfile):
    address = OneToOneField(BasePostalAddress, null=True)
```

## Common Patterns

```python
# Get full address string
full_address = f"{address.street_1}, {address.city}, {address.state} {address.postal_code}"

# Distance calculation
from htk.utils.maths import haversine_distance
distance = haversine_distance(
    lat1, lon1,
    address.latitude, address.longitude
)
```

## Related Modules

- `htk.lib.google.maps` - Maps integration
- `htk.lib.mapbox` - Mapbox integration
