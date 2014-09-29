"""lookup.py

Look up users by various complex logic
"""

from django.contrib.auth import get_user_model

from htk.utils import utcnow

def get_users_currently_at_local_time(lower, upper):
    """Returns a list of Users whose current local time is within a time range

    strategy 1 (inefficient):
    enumerate through every User, and keep the ones whose current local time is within the range

    strategy 2:
    find all the timezones that are in the local time
    query users in that timezone

    `lower` and `upper` are naive datetimes
    """
    UserModel = get_user_model()
    pass
