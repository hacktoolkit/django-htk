import pygeoip

from htk.utils import htk_setting

def get_geoip_country():
    geoip_country_db = htk_setting('HTK_LIB_GEOIP_COUNTRY_DB')
    if geoip_country_db:
        gi_country = pygeoip.GeoIP(geoip_country_db, pygeoip.MEMORY_CACHE)
    else:
        gi_country = None
    return gi_country

def get_geoip_city():
    geoip_city_db = htk_setting('HTK_LIB_GEOIP_CITY_DB')
    if geoip_city_db:
        gi_city = pygeoip.GeoIP(geoip_city_db, pygeoip.MEMORY_CACHE)
    else:
        gi_city = None
    return gi_city
