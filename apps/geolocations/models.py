# Python Standard Library Imports

# Third Party / PIP Imports

# Django Imports
from django.db import models
from django.utils.safestring import mark_safe

# HTK Imports
from htk.apps.geolocations.constants import *
from htk.apps.geolocations.enums import DistanceUnit
from htk.apps.geolocations.utils import get_bounding_box
from htk.apps.geolocations.utils import get_latlng
from htk.apps.geolocations.utils import haversine
from htk.models.classes import HtkBaseModel


class AbstractGeolocation(HtkBaseModel):
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

        NOTE: Do not cache this, as we may (re-)invoke `self.geocode()` within the same session
        """
        result = self.latitude is not None and self.longitude is not None
        return result

    def geocode(self, refresh=False):
        """Geocodes the address
        """
        address = self.get_address_string()
        if not address:
            latitude, longitude = (None, None,)
        else:
            latitude, longitude = get_latlng(address, refresh=refresh)
            if latitude and longitude:
                update_fields = []
                if self.latitude != latitude:
                    self.latitude = latitude
                    update_fields.append('latitude')
                if self.longitude != longitude:
                    self.longitude = longitude
                    update_fields.append('longitude')
                if update_fields:
                    self.save(update_fields=update_fields)
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

    ##
    # Maps

    def map_url(self):
        """Get the Google Maps URL for this geolocation
        """
        url = LOCATION_MAP_URL_FORMAT % self.get_address_string()
        return url

    def geocoordinates_map_url(self):
        """Get the Google Maps URL for this geolocation, using coordinates
        """
        if self.has_latlng():
            lat_lng_str = '%s,%s' % (self.latitude, self.longitude,)
            url = LOCATION_MAP_URL_FORMAT % lat_lng_str
        else:
            url = None
        return url

    def embedded_map_html(self):
        pass

    def embedded_geocoordinates_map_html(self):
        if self.has_latlng():
            from htk.lib.google.utils import get_browser_api_key
            html = """<iframe width="600" height="450" frameborder="0" style="border:0" src="https://www.google.com/maps/embed/v1/place?key=%(api_key)s&q=%(q)s" allowfullscreen></iframe>""" % {
                'api_key' : get_browser_api_key(),
                'q' : '%s,%s' % (self.latitude, self.longitude,),
            }
            html = mark_safe(html)
        else:
            html = None
        return html

    ##
    # Calculations

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

    def distance_from(self, lat, lng):
        """Calculates the distance from this AbstractGeolocation to (`lat`, `lng`)
        """
        distance = haversine(
            lat,
            self.get_latitude(),
            lng,
            self.get_longitude()
        )
        return distance


class BaseUSZipCode(AbstractGeolocation):
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=64, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)

    class Meta:
        abstract = True

    def json_encode(self):
        value = {
            'zip_code' : self.zip_code,
            'state' : self.state,
            'city' : self.city,
            'latitude' : self.latitude,
            'longitude' : self.longitude,
        }
        return value

    def get_address_string(self):
        return self.zip_code
