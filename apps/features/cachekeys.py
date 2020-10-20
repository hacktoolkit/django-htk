# HTK Imports
from htk.cache import CustomCacheScheme
from htk.constants import TIMEOUT_15_MINUTES


class FeatureFlagCache(CustomCacheScheme):
    """Cache management object for Feature Flags
    """
    def get_cache_duration(self):
        duration = TIMEOUT_15_MINUTES
        return duration
