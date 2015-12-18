import rollbar

from htk.utils import htk_setting
from htk.utils.request import get_current_request

def slack_notify(message):
    """Send a Slack notification message
    """
    from htk.lib.slack.utils import webhook_call as slack_webhook_call
    try:
        channel = htk_setting('HTK_SLACK_NOTIFICATIONS_CHANNEL')
        slack_webhook_call(text=message, channel=channel)
    except:
        request = get_current_request()
        rollbar.report_exc_info(request=request)
