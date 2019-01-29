import rollbar

from htk.utils import htk_setting
from htk.utils.request import get_current_request

def slack_notify(message, level=None):
    """Send a Slack notification message

    `level` is one of ['critical', 'severe', 'danger', 'warning', 'info', 'debug',]
    """
    from htk.lib.slack.utils import webhook_call as slack_webhook_call
    try:
        channels = htk_setting('HTK_SLACK_NOTIFICATION_CHANNELS')
        level = level if level in channels else 'info'
        channel = channels.get(level, htk_setting('HTK_SLACK_DEBUG_CHANNEL'))
        slack_webhook_call(text=message, channel=channel)
    except:
        request = get_current_request()
        rollbar.report_exc_info(request=request)
