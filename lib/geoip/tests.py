from django.utils import unittest

from htk.lib.geoip.utils import get_geoip_city
from htk.lib.geoip.utils import get_geoip_country

class GeoIPLibraryTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_geoip_city(self):
        """Test that the client instantiates
        """
        gi_city = get_geoip_city()
        self.assertIsNotNone(gi_city)
        timezone = gi_city.time_zone_by_addr('8.8.8.8')
        self.assertEqual('America/Los_Angeles', timezone)

    def test_get_geoip_country(self):
        """Test that the client instantiates
        """
        gi_country = get_geoip_country()
        self.assertIsNotNone(gi_country)
        country = gi_country.country_code_by_addr('8.8.8.8')
        self.assertEqual('US', country)
