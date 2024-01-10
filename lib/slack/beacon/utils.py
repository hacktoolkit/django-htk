# Django Imports
from django.urls import reverse

# HTK Imports
from htk.utils import htk_setting


def create_slack_beacon(event):
    beacon_key = None
    webhook_settings = event.get('webhook_settings', {})
    slack_webhook_url = webhook_settings.get('slack_webhook_url')
    if slack_webhook_url:
        from uuid import uuid4
        from htk.lib.slack.beacon.cachekeys import SlackBeaconCache
        beacon_key = uuid4().hex[:6]
        payload = {
            'slack_webhook_url' : slack_webhook_url,
            'channel_name' : event.get('channel_name'),
            'user_name' : event.get('user_name'),
        }
        c = SlackBeaconCache(prekey=beacon_key)
        c.cache_store(payload)
    return beacon_key

def create_slack_beacon_url(event):
    """Creates an in-cache homing beacon URL for the user good for 5 minutes
    """
    beacon_url = None
    beacon_url_name = htk_setting('HTK_SLACK_BEACON_URL_NAME')
    if beacon_url_name:
        beacon_key = create_slack_beacon(event)
        if beacon_key:
            webhook_request = event['webhook_request']
            beacon_url = '%(base_uri)s%(beacon_path)s?k=%(beacon_key)s' % {
                'base_uri' : webhook_request['base_uri'],
                'beacon_path' : reverse(beacon_url_name),
                'beacon_key' : beacon_key,
            }
    return beacon_url
