def slack_message_geoip(ip, user_name=None):
    from htk.lib.geoip.utils import get_record_by_ip
    from htk.lib.google.geocode.geocode import reverse_geocode
    from htk.lib.google.maps.utils import get_map_url_for_geolocation
    geoip_record = get_record_by_ip(ip)
    lat = geoip_record.get('latitude')
    lng = geoip_record.get('longitude')
    if lat is None or lng is None:
        msg = 'Could not resolve location from IP'
    else:
        address = reverse_geocode(lat, lng)
        geoip_record['address'] = address
        geoip_record['map_url'] = get_map_url_for_geolocation(lat, lng)
        msg = """*Latitude*: %(latitude)s, *Longitude*: %(longitude)s
*Address*: %(address)s
*Area code*: %(area_code)s
*Map*: %(map_url)s
""" % geoip_record
    geoip_entity = '<@%s> (%s)' % (user_name, ip,) if user_name else ip
    slack_text = '*GeoIP Location for %s*:\n%s' % (
        geoip_entity,
        msg,
    )
    return slack_text
