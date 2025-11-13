# Google Integration

Gmail, Maps, Sheets, Translate, Cloud, and reCAPTCHA APIs.

## Gmail API

```python
from htk.lib.google.gmail.api import GmailAPI

gmail = GmailAPI()
messages = gmail.messages_list()
threads = gmail.threads_list()

# Modify messages
gmail.message_modify(msg_id, add_labels=['LABEL_ID'])
gmail.message_trash(msg_id)
```

## Maps

```python
from htk.lib.google.maps.utils import get_map_url_for_geolocation

# Get Google Maps URL
map_url = get_map_url_for_geolocation(lat=37.7749, lng=-122.4194)
```

## Geocoding

```python
from htk.lib.google.geocode.api import geocode

address = geocode('1600 Pennsylvania Avenue NW, Washington, DC')
# Returns: {'lat': 38.89..., 'lng': -77.03..., ...}
```

## Sheets API

```python
from htk.lib.google.sheets.api import spreadsheets_values_append

# Append to Google Sheet
spreadsheets_values_append(
    spreadsheet_id='sheet_id',
    range='Sheet1!A1',
    values=[['Name', 'Email'], ['John', 'john@example.com']]
)
```

## Translation

```python
from htk.lib.google.translate.utils import translate

result = translate('Hello', source_language='en', target_language='es')
# Returns: 'Hola'
```

## reCAPTCHA

```python
from htk.lib.google.recaptcha.utils import google_recaptcha_site_verification

is_valid = google_recaptcha_site_verification(token)
```

## Configuration

```python
# settings.py
GOOGLE_SERVER_API_KEY = os.environ.get('GOOGLE_SERVER_API_KEY')
GOOGLE_BROWSER_API_KEY = os.environ.get('GOOGLE_BROWSER_API_KEY')
GOOGLE_SHEETS_API_KEY = os.environ.get('GOOGLE_SHEETS_API_KEY')
```
