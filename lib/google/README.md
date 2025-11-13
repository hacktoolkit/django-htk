# Google

## Classes
- **`GmailAPI`** (google/gmail/api.py) - Interface to Gmail API

## Functions
- **`labels_list`** (google/gmail/api.py) - https://developers.google.com/gmail/api/v1/reference/users/labels/list
- **`messages_list`** (google/gmail/api.py) - https://developers.google.com/gmail/api/v1/reference/users/messages/list
- **`message_get`** (google/gmail/api.py) - https://developers.google.com/gmail/api/v1/reference/users/messages/get
- **`message_modify`** (google/gmail/api.py) - Adds or removes labels to a message
- **`message_trash`** (google/gmail/api.py) - https://developers.google.com/gmail/api/v1/reference/users/messages/trash
- **`message_untrash`** (google/gmail/api.py) - https://developers.google.com/gmail/api/v1/reference/users/messages/untrash
- **`threads_list`** (google/gmail/api.py) - https://developers.google.com/gmail/api/v1/reference/users/threads/list
- **`thread_get`** (google/gmail/api.py) - https://developers.google.com/gmail/api/v1/reference/users/threads/get
- **`thread_modify`** (google/gmail/api.py) - Adds or removes labels to a thread
- **`thread_trash`** (google/gmail/api.py) - https://developers.google.com/gmail/api/v1/reference/users/threads/trash
- **`thread_untrash`** (google/gmail/api.py) - https://developers.google.com/gmail/api/v1/reference/users/threads/untrash
- **`get_html`** (google/gmail/api.py) - Returns the HTML part of a message from the API
- **`get_text`** (google/gmail/api.py) - Returns the text part of the message from the API
- **`get_map_url_for_geolocation`** (google/maps/utils.py) - Returns a Google Maps url for `latitude`, `longitude`
- **`google_recaptcha_site_verification`** (google/recaptcha/utils.py) - Gets verification data on a Google Recaptcha response token
- **`spreadsheets_values_append`** (google/sheets/api.py) - https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append
- **`translate`** (google/translate/utils.py) - Translates `term` from `origin` language into `target` language
- **`get_num_server_api_keys`** (google/utils.py) - Returns the number of Google server API keys configured
- **`get_server_api_key`** (google/utils.py) - Retrieves the Google Server API key
- **`get_browser_api_key`** (google/utils.py) - Retrieves the Google Browser API key
