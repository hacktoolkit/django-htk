# Python Standard Library Imports
import json

# Third Party / PIP Imports

# Django Imports

# HTK Imports
from htk.lib.zuora.utils import get_event_name

def default(event_type, payload):
    from htk.utils.debug import slack_debug

    event_name = get_event_name(event_type)
    msg = """%s (`%s`).\nDetails:\n```%s```""" % (
        event_name,
        event_type,
        json.dumps(payload, indent=2),
    )
    slack_debug(msg)

def subscription_created(event_type, payload):
    default(event_type, payload)

    subscription_id = payload['SubscriptionID']
    from htk.lib.zuora.api import HtkZuoraAPI
    api = HtkZuoraAPI()
    subscription = api.get_subscription(subscription_id)
