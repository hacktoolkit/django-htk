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
    COOLDOWN_DURATION_SECONDS = TIMEOUT_24_HOURS

    def get_cache_duration(self):
        duration = self.COOLDOWN_DURATION_SECONDS
        return duration

    def has_cooldown(self):
        """Checks whether cooldown timer is still going
        """
        _has_cooldown = bool(self.get())
        return _has_cooldown

    def reset_cooldown(self, force=False):
        """Resets cooldown timer

        If `force` is `True`, resets the cooldown even there is time remaining.

        Returns whether cooldown was reset, False if timer was still running
        """
        if self.get() and not force:
            was_reset = False
        else:
            self.cache_store()
            was_reset = True

        return was_reset


class BatchRelationshipEmailCooldown(TaskCooldown):
    """Cache management object for not sending out BatchRelationshipEmails too frequently

    Default cooldown: no more than once per day

    prekey = user.id
    """
    COOLDOWN_DURATION_SECONDS = TIMEOUT_24_HOURS

    def get_cache_duration(self):
        duration = self.COOLDOWN_DURATION_SECONDS
        return duration
