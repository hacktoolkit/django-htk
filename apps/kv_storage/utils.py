from htk.apps.kv_storage.cachekeys import KVStorageCache
from htk.utils import htk_setting

def get_kv_storage_model():
    """Gets the key-value storage model class
    """
    model_name = htk_setting('HTK_KV_STORAGE_MODEL', None)
    if model_name:
        from htk.utils.general import resolve_model_dynamically
        KVStorageModel = resolve_model_dynamically(model_name)
    else:
        KVStorageModel = None
    return KVStorageModel

def _get_kv_obj(key):
    """Retrieve the key-value storage model instance for `key`
    """
    KV = get_kv_storage_model()
    kv_obj = None
    if KV:
        try:
            kv_obj = KV.objects.get(key=key)
        except KV.DoesNotExist:
            pass
    return kv_obj

def kv_put(key, value, overwrite=False):
    """PUTs a key-value pair for `key` and `value`

    `overwrite` == True : overwrites if `key` already exists
    `overwrite` == False : raises Exception if `key` already exists
    """
    KV = get_kv_storage_model()
    kv_obj = None
    if KV:
        if overwrite:
            # attempt to retrieve an existing
            kv_obj = _get_kv_obj(key)
            if kv_obj:
                # overwrite the value
                kv_obj.value = value
                kv_obj.save()

        if not kv_obj:
            # overwrite == False or does not already exist
            kv_obj = KV.objects.create(
                key=key,
                value=value
            )

        if kv_obj:
            # update the cache if value was successfully written
            c = KVStorageCache(prekey=key)
            c.cache_store(value)
    return kv_obj

def kv_get(key, cache_only=False, force_refetch=False):
    """GETs the value of `key` from key-value storage

    `cache_only` == True : skips lookup in db, returns the cached value or None
    """
    c = KVStorageCache(prekey=key)
    if force_refetch:
        c.invalidate_cache()
    value = c.get()
    if value is None and not cache_only:
        kv_obj = _get_kv_obj(key)
        if kv_obj:
            value = kv_obj.value
            c.cache_store(value)
    return value

def kv_get_cached(key):
    """GETs the cached value of `key`
    Returns None if not cached
    """
    value = kv_get(key, cache_only=True)
    return value

def kv_delete(key):
    """DELETEs `key` from key-value storage
    """
    c = KVStorageCache(prekey=key)
    c.invalidate_cache()
    kv_obj = _get_kv_obj(key)
    if kv_obj:
        kv_obj.delete()
