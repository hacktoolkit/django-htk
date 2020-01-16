# Django Imports
from django.views.decorators.http import require_GET

# HTK Imports
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
        from htk.lib.slack.messages import slack_message_geoip
        slack_text = slack_message_geoip(ip, beacon['user_name'])
        from htk.lib.slack.utils import webhook_call
        webhook_call(
            webhook_url=beacon['slack_webhook_url'],
            channel=beacon['channel_name'],
            text=slack_text,
        )
        response = json_response_okay()
    else:
        response = json_response_error()
    return response
