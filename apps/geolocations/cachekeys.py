# HTK Imports
from htk.cache import CustomCacheScheme
from htk.constants import *


class GeocodeCache(CustomCacheScheme):
    """Cache management object for geocode lookups
    So we don't hit Google maps geocode too frequently for the same location

    prekey = [<location_name>,]
    """
    def get_cache_duration(self):
        duration = TIMEOUT_1_HOUR
        return duration
