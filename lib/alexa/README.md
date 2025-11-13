# Alexa

## Functions
- **`launch`** (alexa/event_handlers.py) - Launch event handler for Alexa webhook events
- **`default`** (alexa/event_handlers.py) - A Hacktoolkit-flavored default event handler for Alexa webhook events
- **`zesty`** (alexa/event_handlers.py) - Zesty event handler for Alexa skill webhook events
- **`default_event_type_resolver`** (alexa/event_resolvers.py) - The Hacktoolkit-flavored default event type resolver for Alexa webhook events
- **`is_valid_alexa_skill_webhook_event`** (alexa/utils.py) - Determines whether the Alexa skill webhook event is valid
- **`get_event_type`** (alexa/utils.py) - Get event type from Alexa skill webhook `event`
- **`get_event_handlers`** (alexa/utils.py) - Gets all the event handlers available for `event`
- **`get_event_handler_for_type`** (alexa/utils.py) - Gets the event handler for `event_type`
- **`get_event_handler`** (alexa/utils.py) - Gets the event handler for an Amazon Alexa skill webhook event, if available
- **`handle_event`** (alexa/utils.py) - Processes a validated skill request from Amazon Alexa
- **`alexa_skill_webhook_view`** (alexa/views.py) - Handles an Amazon Alexa skill webhook request

## Components
**Views** (`views.py`)
