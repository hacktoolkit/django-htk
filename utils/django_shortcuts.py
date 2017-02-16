def get_object_or_none(cls, *args, **kwargs):
    """Uses get() to return an object, or returns None if the object does not exist.

    `cls` is a Model
    """
    try:
        result = cls.objects.get(*args, **kwargs)
    except:
        result = None
    return result
