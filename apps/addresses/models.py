from django.db import models

class BasePostalAddress(models.Model):
    """Class for storing Postal Address

    This object is always referenced by a foreign key from another object

    Storing address as a separate model is a best practice
    Other than that, there are none. Parsing postal addresses and (even human names, for that matter) are notoriously difficult (not even taking international addresses into consideration)

    http://stackoverflow.com/questions/310540/best-practices-for-storing-postal-addresses-in-a-database-rdbms

    The safest way would be to have a free-form field to enter whatever address, and then an algorithm that can be maintained over time that parses the address into structured fields.

    Right now, go with the "good enough" approach
    """
    street_number = models.CharField(max_length=16, blank=True)
    street = models.CharField(max_length=128, blank=True)
    #unit_type = models.PositiveIntegerField(blank=True, null=True)
    unit = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.CharField(max_length=5, blank=True)
    country = models.CharField(max_length=64, blank=True)

    class Meta:
        abstract = True
        verbose_name = 'Postal Address'
        verbose_name_plural = 'Postal Addresses'

    def __unicode__(self):
        street_component = ' '.join(filter(lambda x: x.strip() != '', [self.street_number, self.street, self.unit,]))
        municipal_component = '%s, %s %s' % (self.city, self.state, self.zipcode,)
        value = '%s, %s' % (street_component, municipal_component,)
        return value

    def clone(self):
        address_clone = PostalAddress.objects.create(
            street_number=self.street_number,
            street=self.street,
            unit=self.unit,
            city=self.city,
            state=self.state,
            zipcode=self.zipcode,
            country=self.country
        )
        return address_clone

    def get_formatted_address(self):
        street_component = ' '.join(filter(lambda x: x.strip() != '', [self.street_number, self.street, self.unit,]))
        municipal_component = '%s, %s %s' % (self.city, self.state, self.zipcode,)
        value = '%s\n%s' % (street_component, municipal_component,)        
        return value

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
