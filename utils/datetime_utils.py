# Python Standard Library Imports
import datetime
import time

# Third Party / PIP Imports
import pytz

# Django Imports
from django.conf import settings
from django.utils.timezone import is_aware
from django.utils.timezone import is_naive
from django.utils.dateparse import parse_datetime as django_parse_datetime

# HTK Imports
from htk.constants.time import *


def utcnow():
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    if settings.TEST:
        from htk.test_scaffold.models import TestScaffold
        fake_time = TestScaffold.get_fake_timestamp()
        if fake_time:
            now = fake_time
    return now


def tznow(timezone_name='America/Los_Angeles'):
    tz = pytz.timezone(timezone_name)
    local_datetime = utcnow().astimezone(tz)
    return local_datetime


def parse_datetime(dt_str):
    return django_parse_datetime(dt_str)


def datetime_to_unix_time(dt):
    """Converts a datetime to a Unix timestamp

    Essentially performs the inverse of datetime.datetime.fromtimestamp(timestamp)

    http://stackoverflow.com/questions/2775864/python-create-unix-timestamp-five-minutes-in-the-future

    Python 3.3 can simply do `dt.timestamp()`

    For Python 2.7, some gymnastics required.

    # TODO: for Python 3 compatibility, check hasattr(dt, 'timestamp') and that it is a method
    """
    if isinstance(dt, datetime.date):
        dt = datetime.datetime.combine(dt, datetime.datetime.min.time())

    if is_aware(dt):
        # convert an aware datetime to UTC first
        dt = dt.astimezone(pytz.utc)
    unix_time = time.mktime(dt.timetuple())
    return unix_time


def unix_time_to_datetime(timestamp, tzinfo=pytz.utc):
    dt = datetime.datetime.fromtimestamp(timestamp).replace(tzinfo=tzinfo)
    return dt


def iso_datetime_to_unix_time(iso):
    """Converts an ISO datetime string to UNIX timestamp
    """
    dt = parse_datetime(iso)
    unix_time = datetime_to_unix_time(dt)
    return unix_time


def iso_to_gregorian(iso_year, iso_week, iso_day):
    """
    Gregorian calendar date for the given ISO year, week and day

    From: https://stackoverflow.com/a/33101215/865091
    """
    # 4th of January always belongs to the same ISO year and Gregorian year
    fourth_jan = datetime.date(iso_year, 1, 4)
    _, fourth_jan_week, fourth_jan_day = fourth_jan.isocalendar()
    delta = datetime.timedelta(
        days=iso_day - fourth_jan_day,
        weeks=iso_week - fourth_jan_week
    )
    gregorian = fourth_jan + delta
    return gregorian


def is_within_hour_bounds_for_timezone(start_hour, end_hour, timezone_name='America/Los_Angeles'):
    """Determine if the local time for given `timezone_name` is currently within `start_hour` and `end_hour` bounds
    """
    local_datetime = tznow(timezone_name)
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

    Morning hours defined as MORNING_HOURS_START to MORNING_HOURS_END (approx: 6:00am to 9:59am)
    """
    is_morning_hours = is_within_hour_bounds(MORNING_HOURS_START, MORNING_HOURS_END, timezone_name=timezone_name)
    return is_morning_hours


def get_timezones_within_current_local_time_bounds(start_hour, end_hour, isoweekdays=None):
    """Get a list of all timezone names whose current local time is within `start_hour` and `end_hour`

    If `isoweekdays` specified, also checks that it falls on one of the days of the week (Monday = 1, Sunday = 7)

    `start_hour` and `end_hour` are naive times
    """
    all_timezones = pytz.all_timezones
    timezone_names = []
    now = utcnow()
    def _is_within_time_bounds(tz_name):
        tz = pytz.timezone(tz_name)
        tz_datetime = now.astimezone(tz)
        result = start_hour <= tz_datetime.hour < end_hour and (isoweekdays is None or now.isoweekday() in isoweekdays)
        return result
    timezone_names = filter(_is_within_time_bounds, all_timezones)
    return timezone_names
