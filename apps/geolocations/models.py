from django.db import models

from htk.apps.geolocations.constants import *
from htk.apps.geolocations.enums import DistanceUnit
from htk.apps.geolocations.utils import get_bounding_box
from htk.apps.geolocations.utils import get_latlng

class AbstractGeolocation(models.Model):
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        abstract = True

    def get_address_string(self):
        """This function needs to be overwritten by the concrete class

        It is called by `self.geocode()` among other callers
        """
        address_string = ''
        return address_string

    def has_latlng(self):
        """Determines whether this object has a latitude and longitude
        """
        result = self.latitude is not None and self.longitude is not None
        return result

    def geocode(self):
        """Geocodes the address
        """
        address = self.get_address_string()
        latitude, longitude = get_latlng(address)
        if latitude and longitude:
            self.latitude = latitude
            self.longitude = longitude
            self.save(update_fields=('latitude', 'longitude',))
        else:
            pass
        return (latitude, longitude,)

    def get_latitude(self):
        """Retrieve the latitude of this object

        Geocodes if the latitude does not exist
        """
        if not self.has_latlng():
            self.geocode()
        return self.latitude

    def get_longitude(self):
        """Retrieve the longitude of this object

        Geocodes if the longititude does not exist
        """
        if not self.has_latlng():
            self.geocode()
        return self.longitude

    def map_url(self):
        """Get the Google Maps URL for this geolocation
        """
        url = LOCATION_MAP_URL_FORMAT % self.get_address_string()
        return url

    @classmethod
    def find_near_latlng(cls, latitude, longitude, distance=DEFAULT_SEARCH_RADIUS, distance_unit=DEFAULT_DISTANCE_UNIT, offset=0, limit=0):
        """Given the geopoint pair `latitude` and `longitude`, find nearby AbstractGeolocation objects of type `cls`

        `distance` a float value
        `distance_unit` the unit for distance. Default is miles, DistanceUnit.MILE
        `offset` use for pagination
        `limit` return a limited number of records

        Naive Algorithm:
        - Calculate a distance matrix for every object and pairing

        Optimized Algorithm:
        - Split up into zones and grids
        - Figure out the bounding box or search radius given the distance from this AbstractGeolocation
        - Find objects within that zone
        """
        (latitude_min, latitude_max, longitude_min, longitude_max,) = get_bounding_box(latitude, longitude, distance=distance, distance_unit=distance_unit)
        nearby_objects = cls.objects.filter(
            latitude__gte=latitude_min,
            latitude__lte=latitude_max,
            longitude__gte=longitude_min,
            longitude__lte=longitude_max
        )
        if limit > 0:
            neaby_objects = nearby_objects[offset:limit]
        return nearby_objects

    @classmethod
    def find_near_location(cls, location_name, distance=DEFAULT_SEARCH_RADIUS, distance_unit=DEFAULT_DISTANCE_UNIT, offset=0, limit=0):
        """Given the geocode-able string `location_name`, find nearby AbstractGeolocation objects of type `cls`

        `distance` a float value
        `distance_unit` the unit for distance. Default is miles, DistanceUnit.MILE
        `offset` use for pagination
        `limit` return a limited number of records
        """
        latitude, longitude = get_latlng(location_name)
        nearby_objects = cls.find_near_latlng(
            latitude,
            longitude,
            distance=distance,
            distance_unit=distance_unit,
            offset=offset,
            limit=limit
        )
        return nearby_objects

    def find_nearby(self, distance=DEFAULT_SEARCH_RADIUS, distance_unit=DEFAULT_DISTANCE_UNIT, cls=None, offset=0, limit=0):
        """Finds nearby AbstractGeolocation objects to this one

        If `cls` is specified, looks for AbstractGeolocation objects of type `cls`, otherwise this class
        `distance` a float value
        `distance_unit` the unit for distance. Default is miles, DistanceUnit.MILE
        `offset` use for pagination
        `limit` return a limited number of records
        """
        if cls is None:
            cls = self.__class__

        nearby_objects = cls.find_near_latlng(
            self.get_latitude(),
            self.get_longitude(),
            distance=distance,
            distance_unit=distance_unit,
            cls=cls,
            offset=offset,
            limit=limit
        )
        return nearby_objects
