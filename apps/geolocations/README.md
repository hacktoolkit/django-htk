# Geolocations

## Classes
- **`GeocodeCache`** (geolocations/cachekeys.py) - Cache management object for geocode lookups

## Functions
- **`get_address_string`** (geolocations/models.py) - This function needs to be overwritten by the concrete class
- **`has_latlng`** (geolocations/models.py) - Determines whether this object has a latitude and longitude
- **`geocode`** (geolocations/models.py) - Geocodes the address
- **`get_latitude`** (geolocations/models.py) - Retrieve the latitude of this object
- **`get_longitude`** (geolocations/models.py) - Retrieve the longitude of this object
- **`map_url`** (geolocations/models.py) - Get the Google Maps URL for this geolocation
- **`geocoordinates_map_url`** (geolocations/models.py) - Get the Google Maps URL for this geolocation, using coordinates
- **`find_near_latlng`** (geolocations/models.py) - Given the geopoint pair `latitude` and `longitude`, find nearby AbstractGeolocation objects of type `cls`
- **`find_near_location`** (geolocations/models.py) - Given the geocode-able string `location_name`, find nearby AbstractGeolocation objects of type `cls`
- **`find_nearby`** (geolocations/models.py) - Finds nearby AbstractGeolocation objects to this one
- **`distance_from`** (geolocations/models.py) - Calculates the distance from this AbstractGeolocation to (`lat`, `lng`)
- **`get_latlng`** (geolocations/utils.py) - Geocodes a `location_name` and caches the result
- **`WGS84EarthRadius`** (geolocations/utils.py) - Earth radius in meters at a given latitude, according to the WGS-84 ellipsoid [m]
- **`convert_distance_to_meters`** (geolocations/utils.py) - Converts `distance` in `distance_unit` to meters
- **`convert_meters`** (geolocations/utils.py) - Converts `distance_meters` in meters to `distance_unit`
- **`get_bounding_box`** (geolocations/utils.py) - Get the bounding box surrounding the point at given coordinates,
- **`haversine`** (geolocations/utils.py) - Calculate the great circle distance between two points
