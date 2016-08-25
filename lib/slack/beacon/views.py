from django.views.decorators.http import require_GET

from htk.api.utils import json_response_error
from htk.api.utils import json_response_okay
from htk.utils.request import extract_request_ip

@require_GET
def slack_beacon_view(request):
    """Receiver for Slack homing beacon
    """

    beacon_key = request.GET.get('k')
    from htk.lib.slack.beacon.cachekeys import SlackBeaconCache
    c = SlackBeaconCache(prekey=beacon_key)
    beacon = c.get()
    ip = extract_request_ip(request)
    if beacon:
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
        slack_text = '*GeoIP Location for %s*:\n%s' % (
            '@%s (%s)' % (beacon['user_name'], ip,),
            msg,
        )

        from htk.lib.slack.utils import webhook_call
        webhook_call(
            webhook_url=beacon['slack_webhook_url'],
            channel=beacon['channel_name'],
            text=slack_text,
            unfurl_links=False,
            unfurl_media=False,
        )
        response = json_response_okay()
    else:
        response = json_response_error()
    return response
