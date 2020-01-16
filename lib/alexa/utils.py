# Python Standard Library Imports
import copy

# Third Party / PIP Imports
#import json
#import requests
import rollbar

# HTK Imports
from htk.utils import htk_setting


def is_valid_alexa_skill_webhook_event(event, request):
    """Determines whether the Alexa skill webhook event is valid

    Mutates `event` by adding `webhook_request` if valid
    """
    is_valid = True
    if is_valid:
        from htk.utils.request import get_request_metadata
        event['webhook_request'] = get_request_metadata(request)
    return is_valid

def get_event_type(event):
    """Get event type from Alexa skill webhook `event`
    """
    event_type_resolver_module_str = htk_setting('HTK_ALEXA_SKILL_EVENT_TYPE_RESOLVER')
    from htk.utils.general import resolve_method_dynamically
    event_type_resolver = resolve_method_dynamically(event_type_resolver_module_str)
    event_type = event_type_resolver(event)
    return event_type

def get_event_handlers(event):
    """Gets all the event handlers available for `event`

    Specifically, this is the set of event handlers in
      {HTK_ALEXA_SKILL_EVENT_HANDLERS}
    """
    event_handlers = copy.copy(htk_setting('HTK_ALEXA_SKILL_EVENT_HANDLERS'))

    # add in additional event group handlers
    extra_event_handlers = htk_setting('HTK_ALEXA_SKILL_EVENT_HANDLERS_EXTRAS')
    for event_group, handlers in extra_event_handlers.items():
        event_handlers.update(handlers)

    return event_handlers

def get_event_handler_for_type(event, event_type=None):
    """Gets the event handler for `event_type`

    `event` is the original Alexa skill webhook event
    """
    if event_type is None:
        event_type = get_event_type(event)
    event_handlers = get_event_handlers(event)
    event_handler_module_str = event_handlers.get(event_type)
    if event_handler_module_str:
        from htk.utils.general import resolve_method_dynamically
        event_handler = resolve_method_dynamically(event_handler_module_str)
    else:
        event_handler = None
    return event_handler

def get_event_handler(event):
    """Gets the event handler for an Amazon Alexa skill webhook event, if available
    """
    event_handler = get_event_handler_for_type(event)
    return event_handler

def handle_event(event):
    """Processes a validated skill request from Amazon Alexa

    Returns a payload if applicable, else None
    """
    event_handler = get_event_handler(event)
    if event_handler:
        try:
            payload = event_handler(event)
        except:
            payload = {
                'version' : '1.0',
                'response' : {
                    'outputSpeech' : {
                        'type' : 'SSML',
                        'ssml' : """<speak>Oops, I couldn't process that.</speak>""",
                    }
                },
            }
            rollbar.report_exc_info(extra_data={
                'event' : event,
                'event_handler' : event_handler.__name__,
            })
    else:
        payload = None
    return payload
