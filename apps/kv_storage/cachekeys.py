# HTK Imports
from htk.cache import CustomCacheScheme
from htk.constants import *


class KVStorageCache(CustomCacheScheme):
    """Cache management object for key-value storage
    """
    def get_cache_duration(self):
        duration = TIMEOUT_30_MINUTES
        return duration
