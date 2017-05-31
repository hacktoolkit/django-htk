from htk.lib.alexa.utils import get_event_handlers

def default_event_type_resolver(event):
    """The Hacktoolkit-flavored default event type resolver for Alexa webhook events
    """
    intent_name = event['request']['intent']['name']
    #(text, command, args,) = parse_event_text(event)
    event_handlers = get_event_handlers(event)
    event_type = intent_name if intent_name in event_handlers else 'default'
    return event_type
