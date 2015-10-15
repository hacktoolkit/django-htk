from htk.lib.slack.utils import parse_event_text
from htk.utils import htk_setting

def default_event_type_resolver(event):
    """The Hacktoolkit-flavored default event type resolver for Slack webhook events
    """
    (text, command, args,) = parse_event_text(event)
    event_handlers = htk_setting('HTK_SLACK_EVENT_HANDLERS')
    event_type = command if command in event_handlers else 'default'
    return event_type
