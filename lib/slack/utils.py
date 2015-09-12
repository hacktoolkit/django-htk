import json
import requests

from htk.utils import htk_setting

def webhook_call(
    webhook_url=None,
    channel=None,
    username=None,
    text='',
    icon_emoji=None
):
    if webhook_url is None:
        webhook_url = htk_setting('HTK_SLACK_WEBHOOK_URL')

    payload = {
        'text' : text,
    }
    if channel:
        payload['channel'] = channel
    if username:
        payload['username'] = username
    if icon_emoji:
        payload['icon_emoji'] = icon_emoji

    #data = 'payload=%s' % json.dumps(payload)
    data = { 'payload' : payload }

    response = requests.post(webhook_url, json=payload)
    return response

def is_valid_webhook_token(token):
    expected_token = htk_setting('HTK_SLACK_WEBHOOK_TOKEN')
    is_valid = token == expected_token
    return is_valid

def default_event_type_resolver(event):
    """The Hacktoolkit-flavored default event type resolver for Slack webhook events
    """
    trigger_word = event['trigger_word']
    text = event['text'][len(trigger_word):].strip()
    event_type = 'default'
    return event_type

def default_event_handler(event):
    """A Hacktoolkit-flavored default event handler for Slack webhook events

    Returns a payload if applicable, or None
    """
    trigger_word = event['trigger_word']
    text = event['text'][len(trigger_word):].strip()

    # for example, we could...
    # make another webhook call in response
    channel = event['channel_id']
    echo_text = 'You said: [%s]. Roger that.' % text
    username = 'Hacktoolkit Bot'
    #webhook_call(text=echo_text, channel=channel, username=username)

    payload = {
        'text' : echo_text,
        'username' : username,
    }
    return payload

def get_event_type(event):
    event_type_resolver_module_str = htk_setting('HTK_SLACK_EVENT_TYPE_RESOLVER')
    from htk.utils.general import resolve_method_dynamically
    event_type_resolver = resolve_method_dynamically(event_type_resolver_module_str)
    event_type = event_type_resolver(event)
    return event_type

def get_event_handler(event):
    """Gets the event handler for a Slack webhook event, if available
    """
    event_handlers = htk_setting('HTK_SLACK_EVENT_HANDLERS')
    event_type = get_event_type(event)
    event_handler_module_str = event_handlers.get(event_type)

    if event_handler_module_str:
        from htk.utils.general import resolve_method_dynamically
        event_handler = resolve_method_dynamically(event_handler_module_str)
    else:
        event_handler = None
    return event_handler

def handle_event(event):
    """Processes a validated webhook request from Slack

    https://api.slack.com/outgoing-webhooks

    Returns a payload if applicable, else None
    """
    event_handler = get_event_handler(event)
    if event_handler:
        payload = event_handler(event)
    else:
        payload = None
    return payload
