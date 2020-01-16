# HTK Imports
from htk.utils import htk_setting


def get_kv_storage_model(namespace=None):
    """Gets the key-value storage model class
    """
    if namespace is None:
        namespace = 'default'
    model_name = htk_setting('HTK_KV_STORAGE_MODELS', {}).get(namespace)
    if model_name:
        from htk.utils.general import resolve_model_dynamically
        KVStorageModel = resolve_model_dynamically(model_name)
    else:
        KVStorageModel = None
    return KVStorageModel

def _get_kv_cache(key, namespace=None):
    from htk.apps.kv_storage.cachekeys import KVStorageCache
    if namespace is None:
        prekey = key
    else:
        prekey = (namespace, key,)
    c = KVStorageCache(prekey=prekey)
    return c

def _get_kv_obj(key, namespace=None):
    """Retrieve the key-value storage model instance for `key`
    """
    KV = get_kv_storage_model(namespace=namespace)
    kv_obj = None
    if KV:
        try:
            kv_obj = KV.objects.get(key=key)
        except KV.DoesNotExist:
            pass
    return kv_obj

def kv_list_keys(namespace=None, prefix=None):
    KV = get_kv_storage_model(namespace=namespace)
    if KV:
        if prefix:
            keys_qs = KV.objects.filter(key__startswith=prefix)
        else:
            keys_qs = KV.objects
        keys = keys_qs.values_list('key', flat=True)
    else:
        keys = []
    return keys

def kv_put(key, value, namespace=None, overwrite=False):
    """PUTs a key-value pair for `key` and `value`

    `overwrite` == True : overwrites if `key` already exists
    `overwrite` == False : raises Exception if `key` already exists
    """
    KV = get_kv_storage_model(namespace=namespace)
    kv_obj = None
    if KV:
        if overwrite:
            # attempt to retrieve an existing
            kv_obj = _get_kv_obj(key, namespace=namespace)
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
            c = _get_kv_cache(key, namespace=namespace)
            c.cache_store(value)
    return kv_obj

def kv_get(key, namespace=None, cache_only=False, force_refetch=False):
    """GETs the value of `key` from key-value storage

    `cache_only` == True : skips lookup in db, returns the cached value or None
    """
    c = _get_kv_cache(key, namespace=namespace)
    if force_refetch:
        c.invalidate_cache()
    value = c.get()
    if value is None and not cache_only:
        kv_obj = _get_kv_obj(key, namespace=namespace)
        if kv_obj:
            value = kv_obj.value
            c.cache_store(value)
    return value

def kv_get_cached(key, namespace=None):
    """GETs the cached value of `key`
    Returns None if not cached
    """
    value = kv_get(key, namespace=namespace, cache_only=True)
    return value

def kv_delete(key, namespace=None):
    """DELETEs `key` from key-value storage
    """
    c = _get_kv_cache(key, namespace=namespace)
    c.invalidate_cache()
    kv_obj = _get_kv_obj(key, namespace=namespace)
    if kv_obj:
        kv_obj.delete()
