LOCATION_MAP_URL_FORMAT = 'https://maps.google.com/?q=%s'

from htk.apps.geolocations.enums import DistanceUnit
DEFAULT_SEARCH_RADIUS = 10
DEFAULT_DISTANCE_UNIT = DistanceUnit.MILE

FEET_PER_MILE = 5280.0
KM_PER_MILE = 1.609344
METERS_PER_KM = 1000.0
MILES_PER_KM = 0.62137119

# Semi-axes of WGS-84 geoidal reference
WGS84_a = 6378137.0  # Major semiaxis [meters]
WGS84_b = 6356752.3142  # Minor semiaxis [meters]
