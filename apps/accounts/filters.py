import datetime

from htk.utils import utcnow

def users_logged_in_within_period(users, window=1):
    """Filter the queryset of users who logged in within the last `window` number of hours.
    """
    threshold = utcnow() - datetime.timedelta(hours=window)
    filtered = users.filter(
        last_login__gte=threshold
    ).order_by(
        '-last_login'
    )
    return filtered

def users_registered_within_period(users, window=1):
    """Filter the queryset of users who registered within the last `window` number of hours.
    """
    threshold = utcnow() - datetime.timedelta(hours=window)
    filtered = users.filter(
        date_joined__gte=threshold
    ).order_by(
        '-date_joined'
    )
    return filtered
