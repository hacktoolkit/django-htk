import rollbar

from htk.lib.alexa.utils import get_event_handlers

def default_event_type_resolver(event):
    """The Hacktoolkit-flavored default event type resolver for Alexa webhook events
    """
    event_handlers = get_event_handlers(event)

    try:
        request = event.get('request', {})
        request_type = request.get('type')
        if request_type == 'LaunchRequest':
            intent_name = 'launch'
        elif request_type == 'IntentRequest':
            intent_name = event['request'].get('intent', {}).get('name', None)
        else:
            intent_name = None
    except:
        from htk.middleware.classes import GlobalRequestMiddleware
        request = GlobalRequestMiddleware.get_current_request()
        extra_data = { 'event' : event, }
        rollbar.report_exc_info(request=request, extra_data=extra_data)

    event_type = intent_name if intent_name in event_handlers else 'default'
    return event_type
