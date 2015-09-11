"""lookup.py

Look up users by various complex logic
"""

from django.contrib.auth import get_user_model

from htk.utils import utcnow
from htk.utils.datetime_utils import get_timezones_within_current_local_time_bounds

def get_all_users(active=True):
    """Returns all users
    """
    UserModel = get_user_model()
    users = UserModel.objects.all()
    if active is not None:
        users = users.filter(is_active=active)
    return users

def get_inactive_users():
    """Returns all inactive users
    """
    UserModel = get_user_model()
    inactive_users = UserModel.objects.filter(is_active=False)
    return inactive_users

def get_users_with_attribute_value(key, value, active=True):
    UserModel = get_user_model()
    users = UserModel.objects.filter(
        attributes__key=key,
        attributes__value=value
    )
    if active is not None:
        users = users.filter(is_active=active)
    return users

def get_users_currently_at_local_time(start_hour, end_hour, isoweekday=None, active=True):
    """Returns a list of Users whose current local time is within a time range

    Strategy 1 (inefficient):
    enumerate through every User, and keep the ones whose current local time is within the range

    Strategy 2:
    - find all the timezones that are in the local time
    - query users in that timezone

    `start_hour` and `end_hour` are naive datetimes
    If `isoweekday` is specified, also checks that it falls on that weekday (Monday = 1, Sunday = 7)
    """
    timezones = get_timezones_within_current_local_time_bounds(start_hour, end_hour, isoweekday=isoweekday)
    UserModel = get_user_model()
    users = UserModel.objects.filter(
        profile__timezone__in=timezones
    )
    if active is not None:
        users = users.filter(is_active=active)
    return users
