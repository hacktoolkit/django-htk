# Python Standard Library Imports

# Third Party / PIP Imports
import rollbar

# HTK Imports
from htk.utils import htk_setting
from htk.utils.notifications import slack_notify


def failed_recaptcha_on_login(user, request=None):
    extra_data = {
        'user' : {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
    }

    message = 'Failed reCAPTCHA. Suspicious login detected.'

    rollbar.report_message(
        message,
        request=request,
        extra_data=extra_data
    )

    if htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED'):
        slack_message = '%s User: %s <%s>' % (
            message,
            user.username,
            user.email,
        )
        slack_notify(slack_message, level='warning')


def failed_recaptcha_on_account_register(request=None):
    message = 'Failed reCAPTCHA. Suspicious account registration detected.'

    rollbar.report_message(message, request=request)

    if htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED'):
        slack_notify(message, level='warning')
