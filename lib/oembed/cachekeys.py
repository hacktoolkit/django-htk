from htk.cache import CustomCacheScheme
from htk.constants.time import *

class OembedResponseCache(CustomCacheScheme):
    def get_cache_duration(self):
        duration = TIMEOUT_30_MINUTES
        return duration
