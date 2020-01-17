# Python Standard Library Imports
import copy
import json

# Third Party (PyPI) Imports
import requests
import rollbar

# HTK Imports
from htk.utils import htk_setting


def webhook_call(
    webhook_url=None,
    channel=None,
    username=None,
    text='',
    attachments=None,
    icon_emoji=None,
    unfurl_links=True,
    unfurl_media=True,
    error_response_handlers=None
):
    """Performs a webhook call to Slack

    https://api.slack.com/incoming-webhooks
    https://api.slack.com/docs/message-formatting

    `channel` override must be a public channel
    """
    if webhook_url is None:
        webhook_url = htk_setting('HTK_SLACK_WEBHOOK_URL')

    payload = {
        'text' : text,
        'unfurl_links' : unfurl_links,
        'unfurl_media' : unfurl_media,
    }
    if channel:
        payload['channel'] = channel
    if username:
        payload['username'] = username
    if icon_emoji:
        payload['icon_emoji'] = icon_emoji
    if attachments:
        payload['attachments'] = attachments

    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        # success case, do nothing
        pass
    elif response.status_code <= 399:
        # 200-300, do nothing
        pass
    else:
        if handle_webhook_error_response(response, error_response_handlers):
            # successfully handled the webhook error
            pass
        else:
            extra_data = {
                'webhook_url' : webhook_url,
                'payload' : payload,
            }
            rollbar.report_message('Slack webhook call error: [%s] %s' % (response.status_code, response.content,), extra_data=extra_data)
    return response

def handle_webhook_error_response(response, error_response_handlers=None):
    """Handles a Slack webhook call error response

    `error_response_handlers` is formatted as:
    {
        404: {
            'No active hooks': <function>,
        },
        500: {
            'channel_not_found': <function>,
        },
    }
    """
    if error_response_handlers is None:
        error_response_handlers = {}

    if response.status_code in error_response_handlers:
        error_message = response.content.strip()
        if error_message in error_response_handlers[response.status_code]:
            handler = error_response_handlers[response.status_code][error_message]
            handler()

def is_valid_webhook_event(event, request):
    """Determines whether the Slack webhook event has a valid token

    Mutates `event` by adding `webhook_settings` if available, and `webhook_request` if valid
    """
    token = event['token']
    expected_token = htk_setting('HTK_SLACK_WEBHOOK_TOKEN')
    is_valid = token == expected_token
    webhook_settings = get_webhook_settings(token)
    event['webhook_settings'] = webhook_settings
    if not is_valid:
        # can still be valid if it has webhook settings for this token
        is_valid = webhook_settings is not None
    else:
        # it's really invalid
        pass
    if is_valid:
        from htk.utils.request import get_request_metadata
        event['webhook_request'] = get_request_metadata(request)
    return is_valid

def get_webhook_settings(token):
    """Retrieves the webhook settings from KV storage
    """
    from htk.apps.kv_storage import kv_get
    key = 'slack_webhook_%s' % token
    webhook_settings = kv_get(key, namespace='slack')
    return webhook_settings

def get_event_type(event):
    """Get event type from Slack webhook `event`
    """
    event_type_resolver_module_str = htk_setting('HTK_SLACK_EVENT_TYPE_RESOLVER')
    from htk.utils.general import resolve_method_dynamically
    event_type_resolver = resolve_method_dynamically(event_type_resolver_module_str)
    event_type = event_type_resolver(event)
    return event_type

def get_event_handlers(event):
    """Gets all the event handlers available for `event`

    Specifically, this is the set of event handlers in
      {HTK_SLACK_EVENT_HANDLERS} + event['webhook_settings']
    """
    event_handlers = copy.copy(htk_setting('HTK_SLACK_EVENT_HANDLERS'))
    webhook_settings = event.get('webhook_settings', {})

    # add in additional event group handlers
    extra_event_handlers = htk_setting('HTK_SLACK_EVENT_HANDLERS_EXTRAS')
    for event_group, handlers in extra_event_handlers.items():
        if webhook_settings.get(event_group, False) is True:
            event_handlers.update(handlers)

    # remove any disabled commands
    disabled_commands = [k for k, v in webhook_settings.items() if v is False and k in event_handlers]
    for command in disabled_commands:
        del event_handlers[command]
    return event_handlers

def get_event_handler_usages(event):
    event_handler_usages = copy.copy(htk_setting('HTK_SLACK_EVENT_HANDLER_USAGES'))
    webhook_settings = event.get('webhook_settings', {})

    # add in additional event group handler usages
    extra_event_handler_usages = htk_setting('HTK_SLACK_EVENT_HANDLER_USAGES_EXTRA')
    for event_group, usages in extra_event_handler_usages.items():
        if webhook_settings.get(event_group, False) is True:
            event_handler_usages.update(usages)
    return event_handler_usages

def is_available_command(event, command):
    """Determines whether `command` is available for the `event`
    """
    event_handler = get_event_handler_for_type(event, event_type=command)
    is_available = event_handler is not None
    return is_available

def get_event_handler_for_type(event, event_type=None):
    """Gets the event handler for `event_type`

    `event` is the original Slack webhook event
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
    """Gets the event handler for a Slack webhook event, if available
    """
    event_handler = get_event_handler_for_type(event)
    return event_handler

def handle_event(event):
    """Processes a validated webhook request from Slack

    https://api.slack.com/outgoing-webhooks

    Returns a payload if applicable, else None
    """
    event_handler = get_event_handler(event)
    if event_handler:
        try:
            payload = event_handler(event)
        except:
            payload = {
                'text' : """Oops, I couldn't process that.""",
            }
            rollbar.report_exc_info(extra_data={
                'event' : event,
                'event_handler' : event_handler.__name__,
            })
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
