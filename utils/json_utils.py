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

            try:
                # check if key is actually a list index
                index = int(level_key)
                node = node[index]
            except (ValueError, KeyError,) as e:
                # key is just a str
                node = node.get(level_key, None)

    return value


def find_all_json_paths(json_obj):
    """Returns all valid JSON paths given a `json_obj`
    """
    paths = []

    def _walk(node, path=''):
        if type(node) == dict:
            for k, v in node.items():
                next_path = '%s.%s' % (path, k,)
                _walk(v, path=next_path)
        elif type(node) == list:
            for v in node:
                _walk(v, path=path)
        elif type(node) in (str, unicode, int,):
            paths.append(path)

    for k, v in json_obj.items():
        _walk(v, k)

    paths = sorted(paths)

    return paths
