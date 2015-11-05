import math

from htk.apps.geolocations.cachekeys import GeocodeCache
from htk.apps.geolocations.constants import *
from htk.apps.geolocations.enums import DistanceUnit
from htk.lib.google.geocode.geocode import get_latlng as get_latlng_google
from htk.utils.maths.trigonometry import deg2rad
from htk.utils.maths.trigonometry import rad2deg

def get_latlng(location_name):
    """Geocodes a `location_name` and caches the result

    For now, uses Google maps geocode API
    """
    c = GeocodeCache(prekey=location_name)
    latlng = c.get()
    if latlng is None:
        latlng = get_latlng_google(location_name)
        c.cache_store(latlng)
    return latlng

def WGS84EarthRadius(lat):
    """Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]

    - http://en.wikipedia.org/wiki/Earth_radius
    - https://en.wikipedia.org/wiki/Great-circle_distance
    """
    An = WGS84_a * WGS84_a * math.cos(lat)
    Bn = WGS84_b * WGS84_b * math.sin(lat)
    Ad = WGS84_a * math.cos(lat)
    Bd = WGS84_b * math.sin(lat)
    radius = math.sqrt( (An*An + Bn*Bn)/(Ad*Ad + Bd*Bd) )
    return radius

def get_bounding_box(latitude, longitude, distance=DEFAULT_SEARCH_RADIUS, distance_unit=DEFAULT_DISTANCE_UNIT):
    """Get the bounding box surrounding the point at given coordinates,
    assuming local approximation of Earth surface as a sphere
    of radius given by WGS84

    `latitude` the search origin latitude in degrees
    `longitude` the search origin longitude in degrees
    `distance` (float) the search radius
    `distance_unit` the unit of measure for the distance

    References:
    - (Source) http://stackoverflow.com/questions/238260/how-to-calculate-the-bounding-box-for-a-given-lat-lng-location (http://stackoverflow.com/a/238558/865091)
    - (See also) http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates
    - (WGS84) https://en.wikipedia.org/wiki/World_Geodetic_System

    Returns a 4-tuples making up 4 points
    """
    lat = deg2rad(latitude)
    lon = deg2rad(longitude)
    if distance_unit == DistanceUnit.MILE:
        distance_meters = distance * KM_PER_MILE * METERS_PER_KM
    elif distance_unit == DistanceUnit.KILOMETER:
        distance_meters = distance * METERS_PER_KM
    elif distance_unit == DistanceUnit.FEET:
        distance_meters = distance / FEET_PER_MILE * KM_PER_MILE * METERS_PER_KM
    elif distance_unit == DistanceUnit.METER:
        distance_meters = distance
    else:
        raise Exception('Unknown distance unit specified: %s' % distance_unit)

    # Radius of Earth at given latitude
    radius = WGS84EarthRadius(lat)
    # Radius of the parallel at given latitude
    pradius = radius * math.cos(lat)

    lat_min = lat - distance_meters / radius
    lat_max = lat + distance_meters / radius
    lon_min = lon - distance_meters / pradius
    lon_max = lon + distance_meters / pradius
    bounding_box = (
        rad2deg(lat_min),
        rad2deg(lat_max),
        rad2deg(lon_min),
        rad2deg(lon_max),
    )
    return bounding_box

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    From: http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points

    References
    - (Source) http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points (http://stackoverflow.com/a/4913653/865091)
    - (Alt) http://stackoverflow.com/a/15737218/865091
    - Also considered: http://www.johndcook.com/blog/python_longitude_latitude/

    Returns distance between two geocoordinates in meters
    """
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    arclength = 2 * math.asin(math.sqrt(a))

    avg_lat = (lat1 + lat2) / 2.0
    radius = WGS84EarthRadius(avg_lat)
    meters = arclength * radius
    return meters
