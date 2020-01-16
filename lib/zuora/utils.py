# Python Standard Library Imports

# HTK Imports
from htk.utils import htk_setting
from htk.utils.general import resolve_method_dynamically


def get_event_name(event_type):
    event_types = htk_setting('HTK_ZUORA_EVENT_TYPES')
    event_name = event_types.get(event_type, 'Unknown event')
    return event_name

def get_event_handler(event_type):
    event_handlers = htk_setting('HTK_ZUORA_EVENT_HANDLERS')
    event_type = event_type if event_type in event_handlers else 'default' if htk_setting('HTK_ZUORA_HANDLE_UNHANDLED_EVENTS') else None
    event_handler_module = event_handlers.get(event_type)
    if event_handler_module:
        event_handler = resolve_method_dynamically(event_handler_module)
    else:
        event_handler = None
    return event_handler
