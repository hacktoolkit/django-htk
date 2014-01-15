from htk.cache import CustomCacheScheme
from htk.constants import *

class StaticAssetVersionCache(CustomCacheScheme):
    """Cache management object for static asset version for CSS and JavaScript

    Usually refreshed at the end of a deploy
    So that client browser cache doesn't have stale JS/CSS after a deploy
    """
    def get_cache_duration(self):
        duration = TIMEOUT_30_DAYS
        return duration
