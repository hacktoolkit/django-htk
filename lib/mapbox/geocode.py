"""
geocode.py
author: Jonathan Tsai <hello@jontsai.com>

Python interface to Mapbox Geocode API

Usage:
    python geocode.py [-g] ADDRESS
    python geocode.py -r LATITUDE LONGITUDE
Examples:
    $ python geocode.py "701 First Ave, Sunnyvale, CA 94089"
    37.4168811,-122.0256155

    $ python geocode.py -r 37.4168811 -122.0256155
    701 1st Avenue, Sunnyvale, CA 94089, USA
"""

# Future Imports
from __future__ import print_function

# Python Standard Library Imports
import getopt
import json
import sys

# Third Party (PyPI) Imports
import requests
from six.moves.urllib.parse import quote

# HTK Imports
from htk.lib.mapbox.utils import get_access_token


# isort: off


# https://docs.mapbox.com/api/search/geocoding/#endpoints
MAPBOX_GEOCODING_API_URL = (
    'https://api.mapbox.com/geocoding/v5/mapbox.places/{resource}'
)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    OPT_STR = 'hgr'
    OPT_LIST = [
        'help',
        'geocode',
        'resolve',
    ]
    is_geocode = True
    if argv is None:
        argv = sys.argv
    try:
        try:
            progname = argv[0]
            opts, args = getopt.getopt(argv[1:], OPT_STR, OPT_LIST)
        except getopt.error as msg:
            raise Usage(msg)
        # process options
        for o, a in opts:
            if o in ('-h', '--help'):
                print(__doc__)
                sys.exit(0)
            elif o in ('-g', '--geocode'):
                is_geocode = True
            elif o in ('-r', '--resolve'):
                is_geocode = False
        if is_geocode and len(args) == 1:
            address = args[0]
            latitude, longitude = get_latlng(address)
            print('{},{}'.format(latitude, longitude))
        elif not is_geocode and len(args) == 2:
            latitude = args[0]
            longitude = args[1]
            address = reverse_geocode(latitude, longitude)
            print(address)
        else:
            raise Usage('Incorrect arguments')

    except Usage as err:
        print(err.msg, file=sys.stderr)
        print('for help use --help', file=sys.stderr)
        return 3.14159


def _report_message(message, level='error', extra_data=None):
    """Wrapper for rollbar.report_message"""
    try:
        import rollbar
        from htk.utils.request import get_current_request

        request = get_current_request()
        rollbar.report_message(
            message, level=level, request=request, extra_data=extra_data
        )
    except:
        pass


def _report_exc_info(extra_data=None):
    """Wrapper for rollbar.report_exc_info"""
    try:
        import rollbar
        from htk.utils.request import get_current_request

        request = get_current_request()
        rollbar.report_exc_info(request=request, extra_data=extra_data)
    except:
        pass


def get_latlng(address):
    extra_data = {
        'address': address,
    }

    resource = '{address}.json'.format(address=quote(address.encode('utf-8')))
    url = MAPBOX_GEOCODING_API_URL.format(resource=resource)

    access_token = get_access_token()
    params = {
        'access_token': access_token,
    }

    response = requests.get(url, params=params)

    if response.status_code == requests.codes.okay:
        # initialize latitude, longitude to None
        latitude = None
        longitude = None

        try:
            extra_data['response_data'] = response.text
            response_json = response.json()

            results = response_json.get('features', [])
            if len(results) > 0:
                result = results[0]
                if result.get('relevance') >= 1:
                    center = result['center']
                    longitude, latitude = center
                else:
                    # did not find an accurate result
                    pass
            else:
                _report_message(
                    'Geocode address failure: No results found',
                    level='info',
                    extra_data=extra_data,
                )
        except ValueError as e:
            # likely to be caused by invalid JSON
            extra_data['error'] = '%s' % e
            _report_exc_info(extra_data=extra_data)
        except KeyError as e:
            # likely to be caused by location missing 'center'
            extra_data['error'] = '%s' % e
            _report_exc_info(extra_data=extra_data)

        latlng = (
            latitude,
            longitude,
        )
    else:
        latlng = None
    return latlng


def reverse_geocode(latitude, longitude):
    extra_data = {
        'latitude': latitude,
        'longitude': longitude,
    }

    resource = '{longitude},{latitude}.json'.format(
        longitude=longitude, latitude=latitude
    )
    url = MAPBOX_GEOCODING_API_URL.format(resource=resource)

    access_token = get_access_token()
    params = {
        'access_token': access_token,
    }

    response = requests.get(url, params=params)
    try:
        extra_data['response_data'] = response.text
        response_json = response.json()

        results = response_json.get('features', [])
        if len(results) > 0:
            result = results[0]
            address = result['place_name']
        else:
            # did not find any results
            address = None
    except KeyError as e:
        address = None
        _report_exc_info(extra_data=extra_data)
    return address


if __name__ == '__main__':
    main()
