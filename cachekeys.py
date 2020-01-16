# HTK Imports
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

class TaskCooldown(CustomCacheScheme):
    """Cache management object for not performing background tasks too frequently

    Default cooldown: no more than once per day
    """
    def get_cache_duration(self):
        duration = TIMEOUT_24_HOURS
        return duration

class BatchRelationshipEmailCooldown(TaskCooldown):
    """Cache management object for not sending out BatchRelationshipEmails too frequently

    Default cooldown: no more than once per day

    prekey = user.id
    """
    def get_cache_duration(self):
        duration = TIMEOUT_24_HOURS
        return duration
