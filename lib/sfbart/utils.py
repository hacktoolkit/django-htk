# Python Standard Library Imports
import datetime

# Third Party / PIP Imports
import pytz

# HTK Imports
from htk.lib.sfbart.api import BartAPI
from htk.lib.sfbart.constants import *
from htk.utils import htk_setting
from htk.utils import utcnow


def get_station_name(station_abbrev):
    station_name = BART_STATION_ABBREVIATIONS.get(station_abbrev, 'Invalid station abbrev: %s' % station_abbrev)
    return station_name

def get_bart_stations():
    stations = [
        { 'abbrev' : station_abbrev, 'name' : get_station_name(station_abbrev), }
        for station_abbrev, station_name
        in BART_STATION_ABBREVIATIONS.items()
    ]
    stations = sorted(stations, key=lambda x: x['name'])
    return stations

def get_bart_schedule_depart(orig_station, dest_station, delay_mins=None):
    api_key = htk_setting('HTK_BART_API_KEY')
    api = BartAPI(api_key)

    if delay_mins:
        now = utcnow().astimezone(pytz.timezone('America/Los_Angeles'))
        depart_time = now + datetime.timedelta(minutes=delay_mins)
        depart_time_str = depart_time.strftime('%I:%M%p').lower()
        api_result = api.get_schedule_depart(orig_station, dest_station, time=depart_time_str, trips_before=0)
    else:
        api_result = api.get_schedule_depart(orig_station, dest_station)

    data = {
        'origin' : orig_station.upper(),
        'destination' : dest_station.upper(),
        'orig_station_name' : get_station_name(orig_station),
        'dest_station_name' : get_station_name(dest_station),
    }
    data.update(api_result)
    return data
