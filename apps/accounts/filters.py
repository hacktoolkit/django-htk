import datetime

from htk.utils import utcnow

def active_users(users, active=True):
    filtered = users.filter(is_active=active)
    return filtered

def inactive_users(users):
    filtered = users.filter(is_active=False)
    return filtered

def users_with_attribute_value(users, key, value):
    filtered = users.filter(
        attributes__key=key,
        attributes__value=value
    )
    return filtered

def users_currently_at_local_time(users, start_hour, end_hour, isoweekdays=None):
    """Filters a QuerySet of `users` whose current local time is within a time range

    Strategy 1 (inefficient):
    enumerate through every User, and keep the ones whose current local time is within the range

    Strategy 2:
    - find all the timezones that are in the local time
    - query users in that timezone

    `start_hour` and `end_hour` are naive datetimes
    If `isoweekdays` is specified, also checks that it falls on one of the days of the week (Monday = 1, Sunday = 7)
    """
    from htk.utils.datetime_utils import get_timezones_within_current_local_time_bounds    
    timezones = get_timezones_within_current_local_time_bounds(start_hour, end_hour, isoweekdays=isoweekdays)
    filtered = users.filter(
        profile__timezone__in=timezones
    )
    return filtered

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
