def get_objects_by_id(object_model, object_ids, strict=False, preserve_ordering=False):
    """Gets a list of Django objects by ids
    If `strict`, all object_ids must exist, or None is returned
    For non `strict`, returns a partial list of Django objects with matching ids
    """
    objects_qs = object_model.objects.filter(id__in=object_ids)
    if strict and objects_qs.count() < len(object_ids):
        objects = None
    else:
        objects = list(objects_qs)
    if objects and preserve_ordering:
        objects = sorted(objects, key=lambda obj: object_ids.index(obj.id))
    else:
        pass
    return objects
