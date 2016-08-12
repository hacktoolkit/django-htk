import pygeoip

from htk.utils import htk_setting

def get_geoip_country():
    geoip_country_db = htk_setting('HTK_LIB_GEOIP_COUNTRY_DB')
    if geoip_country_db:
        gi_country = pygeoip.GeoIP(geoip_country_db)
    else:
        gi_country = None
    return gi_country

def get_geoip_city():
    geoip_city_db = htk_setting('HTK_LIB_GEOIP_CITY_DB')
    if geoip_city_db:
        gi_city = pygeoip.GeoIP(geoip_city_db)
    else:
        gi_city = None
    return gi_city

def get_country_code_by_ip(ip):
    """Returns the country code from `ip`

    http://pygeoip.readthedocs.org/en/v0.3.2/getting-started.html#country-lookup
    """
    country_code = None
    gi_country = get_geoip_country()
    if gi_country:
        country_code = gi_country.country_code_by_addr(ip)
    return country_code

def get_timezone_by_ip(ip):
    """Returns the timezone from `ip`

    http://pygeoip.readthedocs.org/en/v0.3.2/getting-started.html#city-lookup
    """
    timezone = None
    gi_city = get_geoip_city()
    if gi_city:
        timezone = gi_city.time_zone_by_addr(ip)
    return timezone

def get_record_by_ip(ip):
    """Returns dictionary with city data containing country_code, country_name, region, city, postal_code, latitude, longitude, dma_code, metro_code, area_code, region_code and time_zone.

    http://pygeoip.readthedocs.io/en/v0.3.2/api-reference.html#pygeoip.GeoIP.record_by_addr
    """
    gi_city = get_geoip_city()
    record = {}
    if gi_city:
        record = gi_city.record_by_addr(ip)
    return record
