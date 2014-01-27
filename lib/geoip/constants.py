import os

from django.conf import settings

GEOIP_COUNTRY_DB = os.path.join(settings.BASEDIR, '..', 'conf', 'geoip', 'GeoIP.dat')
GEOIP_CITY_DB = os.path.join(settings.BASEDIR, '..', 'conf', 'geoip', 'GeoIPCity.dat')
