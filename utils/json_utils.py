def is_string(thing):
    try:
        # Python 2 has `str` and `unicode`
        return isinstance(thing, basestring)
    except:
        # Python 3
        return isinstance(thing, str)


def find_json_value(json_blob, path):
    """Returns the value at `path` (JSON dot notation) for `json_blob`, a JSON-like `dict`

    Example Usage:

    >>> from htk.utils.json_utils import *
    >>> blob = { 'a': None, 'b': 2, 'c': 3, 'd': None, 'e': { 'f': None, 'g': None, 'i': 9, 'j': 10 }, 'k': ['l', 'm', 'n', 'o', 'p', None, 'r', 's', 't', None, None, 'w', 'x', 'y', 'z']}
    >>> find_json_value(blob, 'a')
    >>> find_json_value(blob, 'b')
    2
    >>> find_json_value(blob, 'c')
    3
    >>> find_json_value(blob, 'd')
    >>> find_json_value(blob, 'e')
    {'f': None, 'g': None, 'i': 9, 'j': 10}
    >>> find_json_value(blob, 'e.f')
    >>> find_json_value(blob, 'e.g')
    >>> find_json_value(blob, 'e.i')
    9
    >>> find_json_value(blob, 'k')
    ['l', 'm', 'n', 'o', 'p', None, 'r', 's', 't', None, None, 'w', 'x', 'y', 'z']
    >>> find_json_value(blob, 'k.0')
    'l'
    >>> find_json_value(blob, 'k.1')
    'm'

    """
    value = None

    node = json_blob
    key = path

    while node is not None and key is not None:
        if isinstance(key, int) and isinstance(node, list):
            try:
                value = node[key]
            except IndexError:
                value = None
            break
        elif isinstance(key, str) and '.' not in key:
            value = node.get(key, None)
            break
        else:
            # traverse to next level
            level_key, key = key.split('.', 1)

            try:
                key = int(key)
            except ValueError:
                pass

            try:
                # check if key is actually a list index
                index = int(level_key)
                node = node[index]
            except (
                ValueError,
                KeyError,
            ) as e:
                # key is just a str
                node = node.get(level_key, None)

    return value


def find_all_json_paths(json_blob):
    """Returns all valid JSON paths given a `json_blob`

    Example Usage:

    >>> from htk.utils.json_utils import find_all_json_paths
    >>> blob = { 'a': None, 'b': 2, 'c': 3, 'd': None, 'e': { 'f': None, 'g': None, 'i': 9, 'j': 10 }, 'k': ['l', 'm', 'n', 'o', 'p', None, 'r', 's', 't', None, None, 'w', 'x', 'y', 'z']}
    >>> find_all_json_paths(blob)
    ['a', 'b', 'c', 'd', 'e', 'e.f', 'e.g', 'e.i', 'e.j', 'k', 'k.0', 'k.1', 'k.10', 'k.11', 'k.12', 'k.13', 'k.14', 'k.2', 'k.3', 'k.4', 'k.5', 'k.6', 'k.7', 'k.8', 'k.9']

    """
    paths = []

    def _build_subpath(suffix, prefix):
        subpath = '%s.%s' % (prefix, suffix) if prefix else suffix
        return subpath

    def _walk(node, path=''):
        if isinstance(node, dict):
            for k, v in node.items():
                next_path = _build_subpath(k, path)
                paths.append(next_path)
                _walk(v, path=next_path)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                next_path = _build_subpath(i, path)
                paths.append(next_path)
                _walk(v, path=next_path)
        elif is_string(node) or isinstance(node, int):
            pass

    _walk(json_blob)

    paths = sorted(paths)
    return paths


def deepcopy_with_compact(json_blob):
    """Performs a deepcopy with `None` values removed from dictionary values and list items

    This function is similar to the built-in `copy.deepcopy` combined with
    Ruby's `Hash.compact` (https://ruby-doc.org/core-2.4.0/Hash.html#method-i-compact)

    This is useful because many APIs do not behave gracefully when `None` is passed into certain fields.

    Example Usage:

    >>> from htk.utils.json_utils import deepcopy_with_compact
    >>> blob = { 'a': None, 'b': 2, 'c': 3, 'd': None, 'e': { 'f': None, 'g': None, 'i': 9, 'j': 10 }, 'k': ['l', 'm', 'n', 'o', 'p', None, 'r', 's', 't', None, None, 'w', 'x', 'y', 'z']}
    >>> blob
    {'a': None, 'b': 2, 'c': 3, 'd': None, 'e': {'f': None, 'g': None, 'i': 9, 'j': 10}, 'k': ['l', 'm', 'n', 'o', 'p', None, 'r', 's', 't', None, None, 'w', 'x', 'y', 'z']}
    >>> deepcopy_with_compact(blob)
    {'b': 2, 'c': 3, 'e': {'i': 9, 'j': 10}, 'k': ['l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'w', 'x', 'y', 'z']}

    """
    if isinstance(json_blob, dict):
        clone = {
            k: deepcopy_with_compact(v)
            for k, v in json_blob.items()
            # just drop the key if the value is `None`
            if v is not None
        }
    elif isinstance(json_blob, list):
        clone = [deepcopy_with_compact(v) for v in json_blob if v is not None]
    else:
        # scalar
        clone = json_blob

    return clone
