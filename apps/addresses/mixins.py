class GoogleLocationMixin(object):
    @property
    def google_location_markup(self):
        markup = {
            '@type': 'Place',
            'address': {
                '@type': 'PostalAddress',
                'streetAddress': self.get_address_street_component(),
                'addressLocality': self.city,
                'addressRegion': self.state,
                'postalCode': self.postal_code,
                'addressCountry': self.country,
            },
        }
        return markup

    def get_static_google_map_image_url(self):
        """
        https://developers.google.com/maps/documentation/staticmaps/

        Example URL:
        http://maps.googleapis.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=13&size=600x300&maptype=roadmap&markers=color:blue%7Clabel:S%7C40.702147,-74.015794&markers=color:green%7Clabel:G%7C40.711614,-74.012318&markers=color:red%7Clabel:C%7C40.718217,-73.998284&sensor=false
        """
        width = 301
        height = 234
        address_str = self.get_address_string()
        base_url = 'http://maps.googleapis.com/maps/api/staticmap?'
        query = urllib.parse.urlencode(
            {
                'center': address_str,
                'markers': 'color:green|%s' % address_str,
                'zoom': 13,
                'size': '%dx%d'
                % (
                    width,
                    height,
                ),
                'maptype': 'roadmap',
                'sensor': 'false',
            }
        )
        url = base_url + query
        return url
