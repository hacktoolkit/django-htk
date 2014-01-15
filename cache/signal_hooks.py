def invalidate_cacheable_object(sender, instance, **kwargs):
    """Generic receiver for CacheableObjects

    Generally called by post_delete signals and some post_save signals
    """
    instance.invalidate_cache()

def refresh_cacheable_object(sender, instance, **kwargs):
    """Generic receiver for CacheableObjects

    Generally called by post_save signals
    """
    instance.cache_store(refresh=True)
