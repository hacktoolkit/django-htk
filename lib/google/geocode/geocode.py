"""
geocode.py
author: Jonathan Tsai <hello@jontsai.com>

Python interface to Google Geocode API

Usage:
    python geocode.py [-g] ADDRESS
    python geocode.py -r LATITUDE LONGITUDE
Examples:
    $ python geocode.py "701 First Ave, Sunnyvale, CA 94089"
    37.4168811,-122.0256155

    $ python geocode.py -r 37.4168811 -122.0256155
    701 1st Avenue, Sunnyvale, CA 94089, USA
"""

import getopt
import json
import requests
import sys
import urllib

GOOGLE_GEOCODING_API_BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/%(format)s?sensor=%(sensor)s&'
GOOGLE_GEOCODING_API_GEOCODE_URL = GOOGLE_GEOCODING_API_BASE_URL + 'address=%(address)s'
GOOGLE_GEOCODING_API_REVERSE_URL = GOOGLE_GEOCODING_API_BASE_URL + 'latlng=%(latlng)s'

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv = None):
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
            opts, args = getopt.getopt(argv[1:],
                                       OPT_STR,
                                       OPT_LIST)
        except getopt.error, msg:
             raise Usage(msg)
        # process options
        for o, a in opts:
            if o in ('-h', '--help'):
                print __doc__
                sys.exit(0)
            elif o in ('-g', '--geocode'):
                is_geocode = True
            elif o in ('-r', '--resolve'):
                is_geocode = False
        if is_geocode and len(args) == 1:
            address = args[0]
            latitude, longitude = get_latlng(address)
            print '%s,%s' % (latitude, longitude,)
        elif not is_geocode and len(args) == 2:
            latitude = args[0]
            longitude = args[1]
            address = reverse_geocode(latitude, longitude)
            print address
        else:
            raise Usage('Incorrect arguments')
                
    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 3.14159

def get_latlng(address):
    address_query = urllib.quote(address, '')
    
    values = {
        'format' : 'json',
        'sensor' : 'false',
        'address' : address_query,
    }
    url = GOOGLE_GEOCODING_API_GEOCODE_URL % values
    response = requests.get(url)
    data = json.loads(response.text)
    try:
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
    except KeyError, k:
        latitude = None
        longitude = None
    return (latitude, longitude,)

def reverse_geocode(latitude, longitude):
    values = {
        'format' : 'json',
        'sensor' : 'false',
        'latlng' : '%s,%s' % (latitude, longitude,)
    }
    url = GOOGLE_GEOCODING_API_REVERSE_URL % values
    response = requests.get(url)
    data = json.loads(response.text)
    try:
        location = data['results'][0]
        address = location['formatted_address']
    except KeyError, k:
        address = None
    return address

if __name__ == '__main__':
    main()
