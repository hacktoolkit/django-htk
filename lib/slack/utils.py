import json
import requests

from htk.apps.kv_storage import *
from htk.utils import htk_setting

def webhook_call(
    webhook_url=None,
    channel=None,
    username=None,
    text='',
    icon_emoji=None
):
    """Performs a webhook call to Slack

    https://api.slack.com/incoming-webhooks

    `channel` override must be a public channel
    """
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
    if not is_valid:
        # try against KV storages
        key = 'slack_webhook_%s' % token
        is_valid = kv_get(key) is not None
    else:
        # it's really invalid
        pass
    return is_valid

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

def parse_event_text(event):
    """Helper function to parse Slack webhook `event` text

    Returns tuple of (text, command, args,)
    """
    trigger_word = event['trigger_word'].lower()
    text = event['text'][len(trigger_word):].strip()
    if trigger_word[-1] == ':':
        trigger_word = trigger_word[:-1]

    if trigger_word in htk_setting('HTK_SLACK_TRIGGER_COMMAND_WORDS'):
        command = trigger_word.lower()
        args = text
    else:
        parts = text.split(' ')
        command = parts[0].lower()
        args = ' '.join(parts[1:]) if len(parts) > 1 else ''
    parsed = (text, command, args,)
    return parsed
