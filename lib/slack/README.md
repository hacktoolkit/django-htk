# Slack

## Classes
- **`SlackBeaconCache`** (slack/beacon/cachekeys.py) - Cache management object for Slack beacon

## Functions
- **`create_slack_beacon_url`** (slack/beacon/utils.py) - Creates an in-cache homing beacon URL for the user good for 5 minutes
- **`slack_beacon_view`** (slack/beacon/views.py) - Receiver for Slack homing beacon
- **`default`** (slack/event_handlers.py) - A Hacktoolkit-flavored default event handler for Slack webhook events
- **`bart`** (slack/event_handlers.py) - BART event handler for Slack webhook events
- **`beacon`** (slack/event_handlers.py) - Beacon geo-ip location handler for Slack webhook events
- **`bible`** (slack/event_handlers.py) - Bible event handler for Slack webhook events
- **`emaildig`** (slack/event_handlers.py) - Email dig event handler for Slack webhook events
- **`findemail`** (slack/event_handlers.py) - Find email event handler for Slack webhook events
- **`geoip`** (slack/event_handlers.py) - GeoIP event handler for Slack webhook events
- **`github_prs`** (slack/event_handlers.py) - Github PR status event handler for Slack webhook events
- **`ohmygreen`** (slack/event_handlers.py) - OhMyGreen event handler for Slack webhook events
- **`stock`** (slack/event_handlers.py) - Stock event handler for Slack webhook events
- **`utcnow_slack`** (slack/event_handlers.py) - utcnow event handler for Slack webhook events
- **`weather`** (slack/event_handlers.py) - Weather event handler for Slack webhook events
- **`zesty`** (slack/event_handlers.py) - Zesty event handler for Slack webhook events
- **`default_event_type_resolver`** (slack/event_resolvers.py) - The Hacktoolkit-flavored default event type resolver for Slack webhook events
- **`webhook_call`** (slack/utils.py) - Performs a webhook call to Slack
- **`handle_webhook_error_response`** (slack/utils.py) - Handles a Slack webhook call error response
- **`is_valid_webhook_event`** (slack/utils.py) - Determines whether the Slack webhook event has a valid token
- **`get_webhook_settings`** (slack/utils.py) - Retrieves the webhook settings from KV storage
- **`get_event_type`** (slack/utils.py) - Get event type from Slack webhook `event`
- **`get_event_handlers`** (slack/utils.py) - Gets all the event handlers available for `event`
- **`is_available_command`** (slack/utils.py) - Determines whether `command` is available for the `event`
- **`get_event_handler_for_type`** (slack/utils.py) - Gets the event handler for `event_type`
- **`get_event_handler`** (slack/utils.py) - Gets the event handler for a Slack webhook event, if available
- **`handle_event`** (slack/utils.py) - Processes a validated webhook request from Slack
- **`parse_event_text`** (slack/utils.py) - Helper function to parse Slack webhook `event` text
- **`slack_webhook_view`** (slack/views.py) - Handles a Slack webhook request

## Components
**Views** (`views.py`)
