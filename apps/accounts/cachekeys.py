from htk.cache import CustomCacheScheme
from htk.constants.time import *

class UserFollowingCache(CustomCacheScheme):
    """Cache management object for user following,
    e.g. user.profile.get_following()

    prekey = user.id
    """
    def get_cache_duration(self):
        duration = TIMEOUT_1_HOUR
        return duration

class UserFollowersCache(CustomCacheScheme):
    """Cache management object for user followers,
    e.g. user.profile.get_followers()

    prekey = user.id
    """
    def get_cache_duration(self):
        duration = TIMEOUT_1_HOUR
        return duration
