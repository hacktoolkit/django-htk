def filter_dict(d, keys):
    """Returns a subset of dictionary `d` with keys from `keys`
    """
    filtered = {}
    for key in keys:
        filtered[key] = d.get(key)
    return filtered

