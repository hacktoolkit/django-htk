import json
import requests

from htk.utils import htk_setting

def get_weather(lat, lng):
    base_url = 'https://api.darksky.net/forecast/%(api_key)s/%(lat)s,%(lng)s'
    #base_url = 'https://api.forecast.io/forecast/%(api_key)s/%(lat)s,%(lng)s'
    api_key = htk_setting('HTK_DARKSKY_API_KEY') or htk_setting('HTK_FORECASTIO_API_KEY')
    url = base_url % {
        'api_key' : api_key,
        'lat' : lat,
        'lng' : lng,
    }
    response = requests.get(url)
    if response.status_code == 200:
        weather = json.loads(response.content)
    else:
        weather = None
    return weather

def format_weather(weather):
    """Returns Dark Sky (formerly ForecastIO) API `weather` formatted as Markdown

    `weather` is the object returned by get_weather()
    """
    currently = weather['currently']
    daily = weather['daily']['data']
    today = daily[0]
    tomorrow = daily[1]
    data = {
        'current_summary' : currently['summary'],
        'current_temp' : currently['temperature'],
        'current_precip_intensity' : currently['precipIntensity'],
        'current_precip_probability' : '%s%%' % (currently['precipProbability'] * 100,),
        'today_summary' : today['summary'],
        'today_temp_max' : today['temperatureMax'],
        'today_temp_min' : today['temperatureMin'],
        'today_precip_intensity' : today['precipIntensity'],
        'today_precip_probability' : '%s%%' % (today['precipProbability'] * 100,),
        'tomorrow_summary' : tomorrow['summary'],
        'tomorrow_temp_max' : tomorrow['temperatureMax'],
        'tomorrow_temp_min' : tomorrow['temperatureMin'],
        'tomorrow_precip_intensity' : tomorrow['precipIntensity'],
        'tomorrow_precip_probability' : '%s%%' % (tomorrow['precipProbability'] * 100,),
    }
    formatted = u"""**Currently**: %(current_temp)s\xB0F (Precip Intensity: %(current_precip_intensity)s, Probability: %(current_precip_probability)s) - %(current_summary)s  
**Today**: %(today_temp_max)sF High, %(today_temp_min)s\xB0F Low (Precip Intensity: %(today_precip_intensity)s, Probability: %(today_precip_probability)s) - %(today_summary)s  
**Tomorrow**: %(tomorrow_temp_max)s\xB0F High, %(tomorrow_temp_min)sF Low (Precip Intensity: %(tomorrow_precip_intensity)s, Probability: %(tomorrow_precip_probability)s) - %(tomorrow_summary)s  
""" % data
    return formatted
