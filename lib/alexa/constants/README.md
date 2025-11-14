# Alexa Constants

Configuration and constants for Amazon Alexa skill integration.

## Configuration Settings

```python
from htk.lib.alexa.constants import (
    HTK_ALEXA_SKILL_EVENT_TYPE_RESOLVER,
    HTK_ALEXA_SKILL_EVENT_HANDLERS,
    HTK_ALEXA_SKILL_EVENT_HANDLERS_EXTRAS,
)
```

### Event Processing

**HTK_ALEXA_SKILL_EVENT_TYPE_RESOLVER**
- Path to function that resolves event types from Alexa requests
- Default: `'htk.lib.alexa.event_resolvers.default_event_type_resolver'`
- This function determines how to route incoming Alexa events

**HTK_ALEXA_SKILL_EVENT_HANDLERS**
- Dictionary mapping event types to handler function paths
- Built-in handlers:
  - `'launch'`: Launch event handler
  - `'default'`: Default fallback handler
  - `'ZestyLunchIntent'`: Intent-specific handler example
- Default handlers located in `htk.lib.alexa.event_handlers`

**HTK_ALEXA_SKILL_EVENT_HANDLERS_EXTRAS**
- Additional custom event handlers for specific intents/events
- Default: `{}` (empty, add custom handlers here)
- Merged with default handlers at runtime

## General Constants

```python
from htk.lib.alexa.constants import (
    ALEXA_SKILL_WEBHOOK_PARAMS,
    PERSONAL_ASSISTANT_PHRASES,
)
```

### Webhook Parameters

**ALEXA_SKILL_WEBHOOK_PARAMS**
- Tuple of required parameters for Alexa skill webhook validation
- Contains: `'session'`, `'request'`, `'version'`
- Used to validate incoming request structure

### Response Phrases

**PERSONAL_ASSISTANT_PHRASES**
- Dictionary of phrase categories with lists of response options
- Categories can be selected based on context/intent
- Example category `'ready'`:
  - "I'm ready to serve."
  - "Your orders are my commands."
  - "What would you like me to help with?"

## Example Usage

```python
from htk.lib.alexa.constants import (
    HTK_ALEXA_SKILL_EVENT_HANDLERS,
    PERSONAL_ASSISTANT_PHRASES,
)

# Get handler for an event type
handler_path = HTK_ALEXA_SKILL_EVENT_HANDLERS.get('launch')

# Get a ready response phrase
ready_phrases = PERSONAL_ASSISTANT_PHRASES['ready']
response = random.choice(ready_phrases)
```

## Configuration in settings.py

```python
HTK_ALEXA_SKILL_EVENT_TYPE_RESOLVER = 'htk.lib.alexa.event_resolvers.default_event_type_resolver'

HTK_ALEXA_SKILL_EVENT_HANDLERS = {
    'launch': 'htk.lib.alexa.event_handlers.launch',
    'default': 'htk.lib.alexa.event_handlers.default',
    'ZestyLunchIntent': 'htk.lib.alexa.event_handlers.zesty',
}

HTK_ALEXA_SKILL_EVENT_HANDLERS_EXTRAS = {
    'CustomIntent': 'myapp.alexa_handlers.custom_intent',
}
```
