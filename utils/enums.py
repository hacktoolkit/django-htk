def enum_to_str(enum_obj):
    """Converts an enum.Enum to a string
    """
    value = ' '.join([word.capitalize() for word in enum_obj.name.split('_')])
    return value
