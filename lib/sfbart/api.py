import requests
from bs4 import BeautifulSoup

from htk.lib.sfbart.constants import *
from htk.lib.sfbart.exceptions import *

class BartAPI(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def make_api_request(self, resource_name, params):
        """Makes an API request to BART API

        Returns a BeautifulSoup of the response XML
        """
        resource_path = BART_API_RESOURCES.get(resource_name, None)
        if resource_path is None:
            raise BartAPIException('Invalid API resource specified: %s' % resource_name)
        url = BART_API_BASE_URL % resource_path
        params['key'] = self.api_key
        response = requests.get(url, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
        else:
            raise BartAPIException('Did not get a valid response from BART API')
        return soup

    def bart_time(self):
        # http://api.bart.gov/docs/overview/barttime.aspx
        pass

    # schedule information
    # http://api.bart.gov/docs/sched/index.aspx

    def _get_schedule_arrive_depart(
        self,
        cmd, # 'arrive' or 'depart'
        orig_station,
        dest_station,
        time='now',
        date='today',
        trips_before=2,
        trips_after=2,
        include_legend=False
    ):
        """Get arrive/depart schedule information
        """
        params = {
            'cmd' : cmd,
            'orig' : orig_station,
            'dest' : dest_station,
            'time' : time,
            'date' : date,
            'b' : trips_before,
            'a' : trips_after,
            'l' : int(include_legend),
        }
        soup = self.make_api_request('schedule_information', params)

        def format_trip_leg(trip_leg_soup):
            # nothing for now
            data = {
            }
            return data

        def format_trip(trip_soup):
            trip_data = {
                'origin' : trip_soup.attrs.get('origin'),
                'destination' : trip_soup.attrs.get('destination'),
                'origTimeMin' : trip_soup.attrs.get('origTimeMin'),
                'origTimeDate' : trip_soup.attrs.get('origTimeDate'),
                'destTimeMin' : trip_soup.attrs.get('destTimeMin'),
                'destTimeDate' : trip_soup.attrs.get('destTimeDate'),
                'tripTime' : trip_soup.attrs.get('tripTime'),
                'legs' : [format_trip_leg(trip_leg_soup) for trip_leg_soup in trip_soup.find_all('leg')],
            }
            return trip_data

        trips = [format_trip(trip_soup) for trip_soup in soup.root.schedule.request.find_all('trip')]
        data = {
            'trips' : trips,
        }
        return data

    def get_schedule_arrive(
        self,
        orig_station,
        dest_station,
        time='now',
        date='today',
        trips_before=2,
        trips_after=2,
        include_legend=False
    ):
        """Get arrive schedule information
        http://api.bart.gov/docs/sched/arrive.aspx
        """
        self._get_schedule_arrive_depart(
            'arrive',
            orig_station,
            dest_station,
            time=time,
            date=date,
            trips_before=trips_before,
            trips_after=trips_after,
            include_legend=include_legend
        )
        return data

    def get_schedule_depart(
        self,
        orig_station,
        dest_station,
        time='now',
        date='today',
        trips_before=1,
        trips_after=3,
        include_legend=False
    ):
        data = self._get_schedule_arrive_depart(
            'depart',
            orig_station,
            dest_station,
            time=time,
            date=date,
            trips_before=trips_before,
            trips_after=trips_after,
            include_legend=include_legend
        )
        return data
