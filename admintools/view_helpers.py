import datetime

from django.contrib.auth import get_user_model

import htk.apps.accounts.filters
from htk.admintools.constants import *
from htk.constants.time import *
from htk.utils import utcnow

def get_pulse_data_users():
    UserModel = get_user_model()
    users = UserModel.objects.all()

    users_registered_last_month = htk.apps.accounts.filters.users_registered_within_period(users, window=HOURS_PER_MONTH)
    users_logged_in_last_month = htk.apps.accounts.filters.users_logged_in_within_period(users, window=HOURS_PER_MONTH)

    recently_joined_users = users_registered_last_month[:PULSE_RECENTLY_JOINED_USERS_LIMIT]
    recent_logins = users_logged_in_last_month[:PULSE_RECENT_LOGINS_LIMIT]

    # registrations
    registrations_last_month = users_registered_last_month.count()
    registrations_last_week = htk.apps.accounts.filters.users_registered_within_period(users_registered_last_month, window=HOURS_PER_WEEK).count()
    registrations_last_day = htk.apps.accounts.filters.users_registered_within_period(users_registered_last_month, window=HOURS_PER_DAY).count()
    registrations_last_hour = htk.apps.accounts.filters.users_registered_within_period(users_registered_last_month, window=1).count()

    # logins
    logins_last_month = users_logged_in_last_month.count()
    logins_last_week = htk.apps.accounts.filters.users_logged_in_within_period(users_logged_in_last_month, window=HOURS_PER_WEEK).count()
    logins_last_day = htk.apps.accounts.filters.users_logged_in_within_period(users_logged_in_last_month, window=HOURS_PER_DAY).count()
    logins_last_hour = htk.apps.accounts.filters.users_logged_in_within_period(users_logged_in_last_month, window=1).count()

    pulse_data = {
        'users' : users.count(),
        'recently_joined_users' : recently_joined_users,
        'recent_logins' : recent_logins,
        # registrations
        'registrations_last_month' : registrations_last_month,
        'registrations_last_week' : registrations_last_week,
        'registrations_last_day' : registrations_last_day,
        'registrations_last_hour' : registrations_last_hour,
        'registrations_last_month_avg_hourly' : format(registrations_last_month / HOURS_PER_MONTH, '.%df' % PULSE_STATS_PRECISION),
        'registrations_last_week_avg_hourly' : format(registrations_last_week / HOURS_PER_WEEK, '.%df' % PULSE_STATS_PRECISION),
        'registrations_last_day_avg_hourly' : format(registrations_last_day / HOURS_PER_DAY, '.%df' % PULSE_STATS_PRECISION),
        # logins
        'logins_last_month' : logins_last_month,
        'logins_last_week' : logins_last_week,
        'logins_last_day' : logins_last_day,
        'logins_last_hour' : logins_last_hour,
        'logins_last_month_avg_hourly' : format(logins_last_month / HOURS_PER_MONTH, '.%df' % PULSE_STATS_PRECISION),
        'logins_last_week_avg_hourly' : format(logins_last_week / HOURS_PER_WEEK, '.%df' % PULSE_STATS_PRECISION),
        'logins_last_day_avg_hourly' : format(logins_last_day / HOURS_PER_DAY, '.%df' % PULSE_STATS_PRECISION),
    }

    return pulse_data
