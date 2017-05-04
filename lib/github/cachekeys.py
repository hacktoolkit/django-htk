from htk.cachekeys import TaskCooldown
from htk.constants.time import *

class GitHubReminderCooldown(TaskCooldown):
    """Cache management object for not performing GitHub reminders for the same user too frequently
    prekey = user.id
    """
    def get_cache_duration(self):
        duration = TIMEOUT_12_HOURS
        return duration
