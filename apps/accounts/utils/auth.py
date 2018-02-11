import rollbar

from django.contrib.auth import login

from htk.utils import htk_setting

def login_authenticated_user(request, authenticated_user):
    """Logs in an authenticated user and performs related updates
    `authenticated_user` has already been authenticated via one of the login backends
    """
    login(request, authenticated_user)
    authenticated_user.profile.update_locale_info_by_ip_from_request(request)

    if htk_setting('HTK_ITERABLE_ENABLED'):
        try:
            from htk.lib.iterable.utils import get_iterable_api_client
            itbl = get_iterable_api_client()
            itbl.notify_login(authenticated_user)
        except:
            rollbar.report_exc_info()
