# Yelp Integration

Business information and review data.

## Quick Start

```python
from htk.lib.yelp.api import business_lookup

# Get business details
business = business_lookup(business_id='google-san-francisco')
print(business['name'], business['rating'], business['reviews'])
```

## Operations

```python
from htk.lib.yelp.utils import YelpAPI

api = YelpAPI()

# Business search
results = api.search('restaurants', location='San Francisco')

# Get reviews
reviews = api.get_reviews(business_id)

# Get photos
photos = api.get_photos(business_id)
```

## Configuration

```python
# settings.py
YELP_API_KEY = os.environ.get('YELP_API_KEY')
```

## Related Modules

- `htk.lib.google` - Maps and location services
- `htk.apps.geolocations` - Location-based features
