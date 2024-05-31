# Python Standard Library Imports
import json

# HTK Imports
from htk.compat import b64encode, b64decode


def build_async_task_result(content, content_type, filename):
    """Builds an Async Task result from JSON

    This is necessary if we want to return multiple values, as the result by default is just a plain string.
    """
    payload = {
        'content': b64encode(content),
        'content_type': content_type,
        'filename': filename,
    }
    result = json.dumps(payload)

    return result


def extract_async_task_result_json_values(result_data):
    """Companion function to perform the inverse of `build_async_task_result()`"""
    payload = json.loads(result_data)

    content = b64decode(payload['content'])

    content_type = payload['content_type']
    filename = payload['filename']

    return (
        content,
        content_type,
        filename,
    )
