import datetime
import pytz

from django.conf import settings
from django.utils.timezone import utc

from htk.constants.time import *

def utcnow():
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    if settings.TEST:
        from htk.test_scaffold.models import TestScaffold
        scaffold = TestScaffold()
        fake_time = scaffold.get_fake_timestamp()
        if fake_time:
            now = fake_time
    return now

def is_within_hour_bounds_for_timezone(start_hour, end_hour, timezone_name='America/Los_Angeles'):
    """Determine if the local time for given `timezone_name` is currently within `start_hour` and `end_hour` bounds
    """
    tz = pytz.timezone(timezone_name)
    local_datetime = utcnow().astimezone(tz)
    is_within_hour_bounds = start_hour <= local_datetime.hour < end_hour
    return is_within_hour_bounds

def is_business_hours_for_timezone(timezone_name='America/Los_Angeles'):
    """Determine if the local time for given `timezone_name` is currently during business hours

    Business hours defined as BUSINESS_HOURS_START to BUSINESS_HOURS_END (approx: 9:00am to 5:59pm)
    """
    is_business_hours = is_within_hour_bounds(BUSINESS_HOURS_START, BUSINESS_HOURS_END, timezone_name=timezone_name)
    return is_business_hours

def is_morning_hours_for_timezone(timezone_name='America/Los_Angeles'):
    """Determine if the local time for given `timezone_name` is currently during morning hours

    Morning hours defined as MORNING_HOURS_START to MORNING_HOURS_END (approx: 6:00am to 8:59pm)
    """
    is_morning_hours = is_within_hour_bounds(MORNING_HOURS_START, MORNING_HOURS_END, timezone_name=timezone_name)
    return is_morning_hours

def get_timezones_within_current_local_time_bounds(start, end, isoweekday=None):
    """Get a list of all timezone names whose current local time is within `start` and `end`

    If `isoweekday` specified, also checks that it falls on that weekday (Monday = 1, Sunday = 7)

    `start` and `end` are naive times
    """
    all_timezones = pytz.all_timezones
    timezone_names = []
    now = utcnow()
    def _is_within_time_bounds(tz_name):
        tz = pytz.timezone(tz_name)
        tz_datetime = now.astimezone(tz)
        result = start < tz_datetime.hour < end and (isoweekday is None or now.isoweekday() == isoweekday)
        return result
    timezone_names = filter(_is_within_time_bounds, all_timezones)
    return timezone_names
