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


def get_latlng(address, min_relevance_threshold=1):
    extra_data = {
        'address': address,
    }

    resource = '{address}.json'.format(address=quote(address))
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
                if result.get('relevance') >= min_relevance_threshold:
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


def fetch_mapbox_reverse_geocode_result(latitude, longitude):
    """
    Fetch the first Mapbox reverse geocode result for a given latitude and longitude

    Example return value:
        >>> fetch_mapbox_geocode_result(37.7749, -122.4194)
        {'address': '1818',
        'center': [-122.41942, 37.774929],
        'context': [{'id': 'neighborhood.601435372',
                    'mapbox_id': 'dXJuOm1ieHBsYzpJOWtzN0E',
                    'text': 'South of Market'},
                    {'id': 'postcode.8939856834013852', 'text': '94102'},
                    {'id': 'place.292358380',
                    'mapbox_id': 'dXJuOm1ieHBsYzpFVzBJN0E',
                    'text': 'San Francisco',
                    'wikidata': 'Q62'},
                    {'id': 'district.20547308',
                    'mapbox_id': 'dXJuOm1ieHBsYzpBVG1HN0E',
                    'text': 'San Francisco County',
                    'wikidata': 'Q62'},
                    {'id': 'region.419052',
                    'mapbox_id': 'dXJuOm1ieHBsYzpCbVRz',
                    'short_code': 'US-CA',
                    'text': 'California',
                    'wikidata': 'Q99'},
                    {'id': 'country.8940',
                    'mapbox_id': 'dXJuOm1ieHBsYzpJdXc',
                    'short_code': 'us',
                    'text': 'United States',
                    'wikidata': 'Q30'}],
        'geometry': {'coordinates': [-122.41942, 37.774929], 'type': 'Point'},
        'id': 'address.8939856834013852',
        'place_name': '1818 Noriega St, San Francisco, California 94102, United '
                    'States',
        'place_type': ['address'],
        'properties': {'accuracy': 'point',
        'mapbox_id': 'dXJuOm1ieGFkcjplNzRmN2U5MC1jODQzLTQxMWQtYTcyMi1mYTQwYTYwMzJjZGI'},
        'relevance': 1,
        'text': 'Noriega St',
        'type': 'Feature'}
    """
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

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        extra_data['response_data'] = response.text
        response_json = response.json()
        results = response_json.get('features', [])

        if len(results) > 0:
            result = results[0]
        else:
            result = None

    except requests.exceptions.RequestException as e:
        extra_data['error'] = f'Request failed: {str(e)}'
        _report_exc_info(extra_data=extra_data)
    except json.JSONDecodeError as e:
        extra_data['error'] = f'Invalid JSON response: {str(e)}'
        _report_exc_info(extra_data=extra_data)
    except Exception as e:
        extra_data['error'] = f'Unexpected error: {str(e)}'
        _report_exc_info(extra_data=extra_data)

    return result


def reverse_geocode(latitude, longitude):
    """
    Reverse geocode a given latitude and longitude and return the address

    Example return value:
        >>> reverse_geocode(37.7749, -122.4194)
        '1818 Noriega St, San Francisco, California 94102, United States'
    """
    result = fetch_mapbox_reverse_geocode_result(latitude, longitude)
    if result:
        address = result.get('place_name')
    else:
        address = None
    return address


def reverse_geocode_with_context(latitude, longitude):
    """Extract location context data from Mapbox reverse geocoding.

    Example:
        >>> reverse_geocode_with_context(37.7749, -122.4194)
        {'country': 'United States',
        'country_short': 'us',
        'district': 'San Francisco County',
        'neighborhood': 'South of Market',
        'place': 'San Francisco',
        'place_name': '1818 Noriega St, San Francisco, California 94102, United '
                    'States',
        'postcode': '94102',
        'region': 'California',
        'region_short': 'US-CA'}
    """
    geocode_result = fetch_mapbox_reverse_geocode_result(latitude, longitude)
    data = {}
    data['place_name'] = geocode_result['place_name']

    # Traverse through context and extract fields
    for field in geocode_result['context']:
        key = field['id'].split('.')[0]
        value = field['text']
        data[key] = value

        if 'short_code' in field:
            key = f'{key}_short'
            value = field['short_code']
            data[key] = value

    return data


if __name__ == '__main__':
    main()
