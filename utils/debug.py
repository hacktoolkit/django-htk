# Django Imports
from django.conf import settings

# HTK Imports
from htk.utils import htk_setting


def slack_debug(message):
    from htk.lib.slack.utils import webhook_call
    channel = htk_setting('HTK_SLACK_DEBUG_CHANNEL')
    webhook_call(text=message, channel=channel)

def show_debug_toolbar(request):
    """Determines whether to show Django Debug Toolbar

    Based on 'debug_toolbar.middleware.show_toolbar'
    """
    try:
        cookie_value = int(request.COOKIES.get('show_debug_toolbar', 0)) == 1
    except ValueError:
        cookie_value = False

    user = request.user
    show = cookie_value and (bool(settings.DEBUG) or (user.is_authenticated() and user.profile and user.profile.is_company_employee))
    return show
