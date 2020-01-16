# HTK Imports
from htk.lib.slack.utils import get_event_handlers
from htk.lib.slack.utils import parse_event_text


def default_event_type_resolver(event):
    """The Hacktoolkit-flavored default event type resolver for Slack webhook events
    """
    (text, command, args,) = parse_event_text(event)
    event_handlers = get_event_handlers(event)
    event_type = command if command in event_handlers else 'default'
    return event_type
