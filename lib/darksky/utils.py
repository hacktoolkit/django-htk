import json
import requests
import rollbar

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

def convert_weather_icon_to_emoji(weather_icon):
    """
    https://darksky.net/dev/docs/response
    http://www.webpagefx.com/tools/emoji-cheat-sheet/
    """
    icons = {
        'default' : ':sunny:',
        'clear-day' : ':sun_small_cloud:',
        'clear-night' : ':night_with_stars:',
        'rain' : ':rain_cloud:',
        'snow' : ':snow_cloud:',
        'sleet' : ':snow_cloud:', # TODO better icon
        'wind' : ':wind_chime:',
        'fog' : ':fog:',
        'cloudy' : ':cloud:',
        'partly-cloudy-day' : ':partly_sunny:',
        'partly-cloudy-night' : ':night_with_stars:', # TODO better icon
        'hail' : ':snow_cloud:', # TODO better icon
        'thunderstorm' : ':thunder_cloud_and_rain:',
        'tornado' : ':tornado:',
    }
    if weather_icon not in icons:
        weather_icon = 'default'
        rollbar.report_message('Unmatched weather icon: %s' % weather_icon)
    icon = icons.get(weather_icon)
    return icon

def _extract_period_weather(period_weather, prefix):
    """Returns a dictionary of relevant weather data from `period_weather`, with keys prefixed with `prefix`
    """
    precip_probability = period_weather['precipProbability']
    data = {
        prefix + '_summary' : period_weather['summary'],
        prefix + '_icon' : convert_weather_icon_to_emoji(period_weather['icon']),
        prefix + '_precip_intensity' : period_weather['precipIntensity'],
        prefix + '_precip_probability' : '%s%%' % (precip_probability * 100,),
    }
    # weather['currently'] only
    if period_weather.get('temperature'):
        data[prefix + '_temp'] = period_weather['temperature']
    # weather['daily']['data'][n] only
    if period_weather.get('temperatureMax'):
        data[prefix + '_temp_max'] = period_weather['temperatureMax']
    if period_weather.get('temperatureMin'):
        data[prefix + '_temp_min'] = period_weather['temperatureMin']

    # rain alert
    RAIN_ALERT_THRESHOLD = 0.15
    if precip_probability > RAIN_ALERT_THRESHOLD:
        data['rain_alert'] = '\n@here **ALERT!** Likelihood of rain!'
    return data

def format_weather(weather):
    """Returns Dark Sky (formerly ForecastIO) API `weather` formatted as Markdown

    `weather` is the object returned by get_weather()
    """
    daily = weather['daily']['data']

    data = {
        'rain_alert' : '',
    }
    data.update(_extract_period_weather(weather['currently'], 'current'))
    data.update(_extract_period_weather(daily[0], 'today'))
    data.update(_extract_period_weather(daily[1], 'tomorrow'))

    formatted = u"""**Currently**: %(current_temp)s\xB0F (Precip Intensity: %(current_precip_intensity)s, Probability: %(current_precip_probability)s) - %(current_summary)s %(current_icon)s  
**Today**: %(today_temp_max)sF High, %(today_temp_min)s\xB0F Low (Precip Intensity: %(today_precip_intensity)s, Probability: %(today_precip_probability)s) - %(today_summary)s %(today_icon)s  
**Tomorrow**: %(tomorrow_temp_max)s\xB0F High, %(tomorrow_temp_min)sF Low (Precip Intensity: %(tomorrow_precip_intensity)s, Probability: %(tomorrow_precip_probability)s) - %(tomorrow_summary)s %(tomorrow_icon)s  
%(rain_alert)s
""" % data
    return formatted
