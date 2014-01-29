from htk.cache import CustomCacheScheme
from htk.constants.time import *

class S3UrlCache(CustomCacheScheme):
    """Cache management object for url of object stored in Amazon S3

    We typically request Amazon S3 URLs for 1 hour, but it could expire earlier than that. So we cache for 30 minutes to be safe, and in practice, even less.

    Calls to self.cache_store() should specify `duration`
    """
    def get_cache_duration(self):
        duration = TIMEOUT_30_MINUTES
        return duration
