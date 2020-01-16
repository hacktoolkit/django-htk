# HTK Imports
from htk.apps.accounts.utils.general import get_user_by_id
from htk.apps.kv_storage import *
from htk.lib.plivo.constants import *


def get_plivo_number_owner(number):
    """Retrieves the User that owns `number`
    """
    key = 'plivo_owner_%s' % number
    owner_id = kv_get(key)
    if owner_id:
        user = get_user_by_id(owner_id)
    else:
        user = None
    return user

def handle_message_event(event):
    """Handles a Plivo message event
    """
    incoming_number = event['To']
    user = get_plivo_number_owner(incoming_number)
    if user:
        slack_webhook_url = user.profile.get_attribute('plivo_slack_webhook_url')
        message_format = user.profile.get_attribute('plivo_slack_message_format') or PLIVO_SLACK_DEFAULT_MESSAGE_FORMAT
        message = message_format % event
        from htk.lib.slack.utils import webhook_call
        webhook_response = webhook_call(
            webhook_url=slack_webhook_url,
            text=message
        )
        result = True
    else:
        result = False
    return result
