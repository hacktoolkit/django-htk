# HTK Imports
from htk.utils import htk_setting
from htk.utils.datetime_utils import localized_datetime
from htk.utils.users import get_authenticated_user


def get_local_time(dt=None, user=None):
    """Converts a datetime `dt` to the local timezone of `user`
    """
    if user is None:
        user = get_authenticated_user()

    if user:
        local_time = user.profile.get_local_time(dt=dt)
    else:
        local_time = dt

    return local_time


def localized_time_for_user(naive_dt, user=None):
    """Attaches a timezone for `user` to `naive_dt`

    This function is typically used for processing UGC datetimes
    """
    if user is None:
        user = get_authenticated_user()

    if user:
        timezone_name = user.profile.get_timezone()
    else:
        timezone_name = htk_setting('HTK_DEFAULT_TIMEZONE', 'UTC')

    dt = localized_datetime(naive_dt, timezone_name=timezone_name)
    return dt
