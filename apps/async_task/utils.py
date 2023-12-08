# Python Standard Library Imports
import base64
import json


def build_async_task_result(content, content_type, filename):
    """Builds an Async Task result from JSON

    This is necessary if we want to return multiple values, as the result by default is just a plain string.
    """
    b64encoded_content = base64.b64encode(content.encode('utf-8'))

    # Python 2 returns ``str`` and Python 3 returns ``bytes``
    if isinstance(b64encoded_content, bytes):
        b64encoded_content = b64encoded_content.decode('utf-8')

    payload = {
        'content': b64encoded_content,
        'content_type': content_type,
        'filename': filename,
    }
    result = json.dumps(payload)
    return result


def extract_async_task_result_json_values(result_data):
    """Companion function to perform the inverse of `build_async_task_result()`"""
    payload = json.loads(result_data)

    content = base64.b64decode(payload['content'].encode('utf-8'))
    if isinstance(content, bytes):
        content = content.decode('utf-8')

    content_type = payload['content_type']
    filename = payload['filename']

    return (
        content,
        content_type,
        filename,
    )
