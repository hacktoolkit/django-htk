def get_map_url_for_geolocation(latitude, longitude):
    """Returns a Google Maps url for `latitude`, `longitude`
    """
    values = {
        'latitude' : latitude,
        'longitude' : longitude,
    }
    url = 'https://www.google.com/maps/place/%(latitude)s,%(longitude)s/@%(latitude)s,%(longitude)s,17z' % values
    return url
