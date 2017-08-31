from django.db import models

from htk.apps.addresses.enums import AddressUnitType
from htk.apps.addresses.utils import get_unit_type_choices
from htk.apps.geolocations.models import AbstractGeolocation

class BasePostalAddress(AbstractGeolocation):
    """Class for storing Postal Address

    This object is always referenced by a foreign key from another object

    Storing address as a separate model is a best practice
    Other than that, there are none. Parsing postal addresses and (even human names, for that matter) are notoriously difficult (not even taking international addresses into consideration)

    http://stackoverflow.com/questions/310540/best-practices-for-storing-postal-addresses-in-a-database-rdbms

    The safest way would be to have a free-form field to enter whatever address, and then an algorithm that can be maintained over time that parses the address into structured fields.

    Right now, go with the "good enough" approach
    """
    name = models.CharField(max_length=64, blank=True)
    street = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.CharField(max_length=5, blank=True)
    country = models.CharField(max_length=64, blank=True)
    # parts
    street_number = models.CharField(max_length=16, blank=True)
    street_name = models.CharField(max_length=64, blank=True)
    unit_type = models.PositiveIntegerField(default=AddressUnitType.NONE.value, choices=get_unit_type_choices())
    unit = models.CharField(max_length=10, blank=True)

    class Meta:
        abstract = True
        verbose_name = 'Postal Address'
        verbose_name_plural = 'Postal Addresses'

    def __unicode__(self):
        value = self.get_address_string()
        return value

    def clone(self):
        address_clone = PostalAddress.objects.create(
            street=self.street,
            city=self.city,
            state=self.state,
            zipcode=self.zipcode,
            country=self.country,
            street_number=self.street_number,
            street_name=self.street_name,
            unit_type=self.unit_type,
            unit=self.unit,
            latitude=self.latitude,
            longitude=self.longitude
        )
        return address_clone

    ##
    # address formats

    def get_address_street_component(self):
        if self.street_number and self.street_name:
            from htk.utils.enums import enum_to_str
            if self.unit_type == AddressUnitType.HASH:
                unit_type = '#'
            elif self.unit_type > 0:
                unit_type = enum_to_str(AddressUnitType(self.unit_type))
            else:
                unit_type = ''

            street_component = ' '.join(
                filter(
                    lambda x: x.strip() != '',
                    [
                        self.street_number,
                        self.street_name,
                        unit_type,
                        self.unit,
                    ]
                )
            )
        else:
            street_component = self.street
        return street_component

    def get_address_municipal_component(self):
        municipal_component = '%s, %s %s' % (self.city, self.state, self.zipcode,)
        return municipal_component

    def get_address_string(self):
        street_component = self.get_address_street_component()
        municipal_component = self.get_address_municipal_component()
        address_string = '%s, %s' % (street_component, municipal_component,)
        return address_string

    def get_formatted_address(self):
        street_component = self.get_address_street_component()
        municipal_component = self.get_address_municipal_component()
        formatted = '%s\n%s' % (street_component, municipal_component,)        
        return formatted

    ##
    # utils

    def get_static_google_map_image_url(self):
        """
        https://developers.google.com/maps/documentation/staticmaps/

        Example URL:
        http://maps.googleapis.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=13&size=600x300&maptype=roadmap&markers=color:blue%7Clabel:S%7C40.702147,-74.015794&markers=color:green%7Clabel:G%7C40.711614,-74.012318&markers=color:red%7Clabel:C%7C40.718217,-73.998284&sensor=false
        """
        width = 301
        height = 234
        str_value = self.__unicode__()
        base_url = 'http://maps.googleapis.com/maps/api/staticmap?'
        query = urllib.urlencode(
            {
                'center': str_value,
                'markers': 'color:green|%s' % str_value,
                'zoom': 13,
                'size': '%dx%d' % (width, height,),
                'maptype': 'roadmap',
                'sensor': 'false',
            }
        )
        url = base_url + query
        return url
