"""lookup.py

Look up users by various complex logic
"""

from django.contrib.auth import get_user_model

import htk.apps.accounts.filters as _filters
from htk.utils import utcnow
from htk.utils.datetime_utils import get_timezones_within_current_local_time_bounds

def get_all_users(active=True):
    """Returns all users
    """
    UserModel = get_user_model()
    users = UserModel.objects.all()
    if active is not None:
        users = _filters.active_users(users, active=active)
    return users

def get_inactive_users():
    """Returns all inactive users
    """
    UserModel = get_user_model()
    inactive_users = _filters.inactive_users(UserModel.objects)
    return inactive_users

def get_users_with_attribute_value(key, value, active=True):
    UserModel = get_user_model()
    users = _filters.users_with_attribute_value(UserModel.objects, key, value)
    if active is not None:
        users = _filters.active_users(users, active=active)
    return users

def get_users_currently_at_local_time(start_hour, end_hour, isoweekdays=None, active=True):
    """Returns a Queryset of Users whose current local time is within a time range

    `start_hour` and `end_hour` are naive datetimes
    If `isoweekdays` is specified, also checks that it falls on one of the days of the week (Monday = 1, Sunday = 7)
    """
    timezones = get_timezones_within_current_local_time_bounds(start_hour, end_hour, isoweekdays=isoweekdays)
    UserModel = get_user_model()
    users = _filters.users_currently_at_local_time(
        UserModel.objects,
        start_hour,
        end_hour,
        isoweekdays=isoweekdays
    )

    if active is not None:
        users = _filters.active_users(users, active=active)
    return users
