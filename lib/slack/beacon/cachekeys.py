from htk.cache import CustomCacheScheme
from htk.constants.time import *

class SlackBeaconCache(CustomCacheScheme):
    """Cache management object for Slack beacon
    """
    def get_cache_duration(self):
        duration = TIMEOUT_5_MINUTES
        return duration
