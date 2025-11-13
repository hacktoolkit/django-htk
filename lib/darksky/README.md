# Forecastio Integration

Weather forecasting (now Darksky).

## Quick Start

```python
from htk.lib.darksky.utils import generate_weather_report

# Forecastio is the predecessor to Darksky
weather_data = get_weather(lat, lon)
report = generate_weather_report(weather_data)
```

## Configuration

```python
# settings.py
DARKSKY_API_KEY = os.environ.get('DARKSKY_API_KEY')
```

## Related Modules

- `htk.lib.darksky` - Current weather API
