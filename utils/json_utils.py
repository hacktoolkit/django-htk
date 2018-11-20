def find_json_value(obj, path):
    """Returns the value at `path` (JSON dot notation) for `obj`, a JSON-like `dict`
    """
    value = None

    node = obj
    key = path

    while node and key:
        if key in node:
            value = node[key]
            break
        else:
            # traverse to next level
            parts = key.split('.')

            level_key = parts[0]
            key = '.'.join(parts[1:])

            node = node.get(level_key, None)

    return value
