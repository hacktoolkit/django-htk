# Python Standard Library Imports
import base64

# Third Party / PIP Imports

# HTK Imports

def get_message_html(message):
    """Returns the HTML part of a message from the API

    https://developers.google.com/gmail/api/v1/reference/users/messages/get
    """
    html_part = None
    for part in message['payload']['parts']:
        if part['mimeType'] == 'text/html':
            html_part = part
            break

    if html_part:
        message_body_data = html_part['body']['data']
        message_html = base64.b64decode(message_body_data.replace('-', '+').replace('_', '/'))
    else:
        message_html = None

    return message_html
