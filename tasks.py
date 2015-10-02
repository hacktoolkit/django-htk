import inspect

class BaseTask(object):
    """Base class for background tasks

    Examples:
    - Daily or weekly updates
    - Drip reminders
    - Account status reports
    - Shopping cart abandonment reminders
    """
    def __init__(self, cooldown_class=None):
        # set cooldown_class
        from htk.cachekeys import TaskCooldown
        if inspect.isclass(cooldown_class) and issubclass(cooldown_class, TaskCooldown):
            self.cooldown_class = cooldown_class
        else:
            self.cooldown_class = TaskCooldown

    def get_cooldown_class_prekey(self, user):
        prekey = user.id
        return prekey

    def has_cooldown(self, user):
        """Checks whether cooldown timer is still going for `user`
        """
        prekey = self.get_cooldown_class_prekey(user)
        c = self.cooldown_class(prekey)
        _has_cooldown = bool(c.get())
        return _has_cooldown

    def reset_cooldown(self, user):
        """Resets cooldown timer for this `user`

        Returns whether cooldown was reset, False if timer was still running
        """
        prekey = self.get_cooldown_class_prekey(user)
        c = self.cooldown_class(prekey)
        if c.get():
            was_reset = False
        else:
            c.cache_store()
            was_reset = True
        return was_reset

    def get_users(self):
        """Returns a list or QuerySet of User objects

        Should be overridden
        """
        users = []
        return users

    def execute(self, uesr):
        """Workhorse function called by `self.execute_batch`

        Can be overriden
        """
        pass

    def execute_batch(self):
        """Batch execution
        """
        users = self.get_users()
        for user in users:
            if self.has_cooldown(user):
                # cooldown has not elapsed yet, don't execute too frequently
                pass
            else:
                self.execute(user)
                # cache right after execution, not before
                # since each execution costs a non-zero overhead
                self.reset_cooldown(user)
