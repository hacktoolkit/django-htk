# Python Standard Library Imports

# Third Party / PIP Imports

# HTK Imports
from htk.lib.yahoo.groups.message import YahooGroupsMessage

def yahoo_groups_message_parser(message_html):
    """Extracts the main message from a Yahoo Groups message
    """
    yahoo_groups_message = YahooGroupsMessage(message_html)

    message = yahoo_groups_message.message
    return message
