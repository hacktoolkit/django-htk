# Third Party / PIP Imports
import rollbar

# HTK Imports
from htk.utils import htk_setting


def notify_user_email_update(user, old_email, new_email):
    if htk_setting('HTK_ITERABLE_ENABLED'):
        try:
            from htk.lib.iterable.utils import get_iterable_api_client
            itbl = get_iterable_api_client()
            itbl.update_user_email(old_email, new_email, force=True)
        except:
            rollbar.report_exc_info()
