from htk.lib.forecastio.utils import get_weather as get_weather_forecastio
from htk.lib.google.geocode.geocode import get_latlng

def get_weather(location):
    """Gets weather for a `location`

    `location` needs to be a geocode-able string
    """
    location = str(location)
    latitude, longitude = get_latlng(location)
    weather = get_weather_forecastio(latitude, longitude)
    return weather
