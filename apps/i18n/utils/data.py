# Python Standard Library Imports
import json
import os

# HTK Imports
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)


def retrieve_all_strings():
    LocalizableString = resolve_model_dynamically(
        htk_setting('HTK_LOCALIZABLE_STRING_MODEL')
    )
    localizable_strings = LocalizableString.objects.order_by('key')
    data = {
        localizable_string.key: localizable_string.json_encode(
            include_key=False
        )['translations']
        for localizable_string in localizable_strings
    }

    return data


def dump_strings(file_path, indent=4):
    data = retrieve_all_strings()

    dir_name = os.path.dirname(file_path)
    os.makedirs(dir_name, exist_ok=True)

    with open(file_path, 'w') as f:
        f.write(json.dumps(data, indent=indent))
        f.write('\n')

    num_strings = len(data)
    return num_strings
