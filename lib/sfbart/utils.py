from htk.lib.sfbart.api import BartAPI
from htk.lib.sfbart.constants import *
from htk.utils import htk_setting

def get_station_name(station_abbrev):
    station_name = BART_STATION_ABBREVIATIONS.get(station_abbrev, 'Invalid station abbrev: %s' % station_abbrev)
    return station_name

def get_bart_stations():
    sorted_station_abbrevs = sorted(BART_STATION_ABBREVIATIONS.iterkeys())
    stations = [
        { 'abbrev' : station_abbrev, 'name' : get_station_name(station_abbrev), }
        for station_abbrev
        in sorted_station_abbrevs
    ]
    return stations

def get_bart_schedule_depart(orig_station, dest_station):
    api_key = htk_setting('HTK_BART_API_KEY')
    api = BartAPI(api_key)
    api_result = api.get_schedule_depart(orig_station, dest_station)
    data = {
        'origin' : orig_station.upper(),
        'destination' : dest_station.upper(),
        'orig_station_name' : get_station_name(orig_station),
        'dest_station_name' : get_station_name(dest_station),
    }
    data.update(api_result)
    return data

