# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.conf import settings

# HTK Imports
from htk.utils import htk_setting
from htk.utils.request import get_current_request


# isort: off


def notify(message, level=None, use_messages=True, use_slack=None):
    """Wrapper for simultaneously sending a message via:

    - Django messages framework (https://docs.djangoproject.com/en/4.1/ref/contrib/messages/)
    - Slack notification

    `level` is one of ['critical', 'severe', 'danger', 'warning', 'info', 'debug',]
    """

    if use_messages:
        from django.contrib import messages

        MESSAGES_LEVEL_MAP = {
            'critical': messages.ERROR,
            'severe': messages.ERROR,
            'danger': messages.WARNING,
            'warning': messages.WARNING,
            'info': messages.INFO,
            'debug': messages.DEBUG,
        }

        request = get_current_request()
        default_level = (
            'debug' if (settings.ENV_DEV or settings.TEST) else 'info'
        )
        level = level if level in MESSAGES_LEVEL_MAP else default_level
        message_level = MESSAGES_LEVEL_MAP[level]
        messages.add_message(request, message_level, message)

    if use_slack is None:
        use_slack = htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED')

    if use_slack:
        slack_notify(message, level=level)


def slack_notify(message, level=None, custom_channel=None):
    """Send a Slack notification message

    `level` is one of ['critical', 'severe', 'danger', 'warning', 'info', 'debug',]
    `custom_channel` is a string of a custom Slack channel name
    """
    from htk.lib.slack.utils import webhook_call as slack_webhook_call

    try:
        channels = htk_setting('HTK_SLACK_NOTIFICATION_CHANNELS')
        default_level = (
            'debug' if (settings.ENV_DEV or settings.TEST) else 'info'
        )
        level = level if level in channels else default_level
        channel = custom_channel or channels.get(level, htk_setting('HTK_SLACK_DEBUG_CHANNEL'))
        slack_webhook_call(text=message, channel=channel)
    except:
        request = get_current_request()
        rollbar.report_exc_info(request=request)
