# Python Standard Library Imports
from functools import wraps

# Third Party (PyPI) Imports
import rollbar

# HTK Imports
from htk.cachekeys import TaskCooldown
from htk.utils import htk_setting
from htk.utils.notifications import slack_notify
from htk.utils.timer import HtkTimer

from celery import shared_task


class safe_timed_task(object):
    def __init__(self, task_name, notify=False, cooldown_secs=None, force_cooldown=False):
        self.task_name = task_name
        self.notify = notify
        self.cooldown_secs = cooldown_secs
        self.force_cooldown = force_cooldown

    @property
    def cooldown_class(self):
        if self.cooldown_secs is not None:
            class _Cooldown(TaskCooldown):
                COOLDOWN_DURATION_SECONDS = self.cooldown_secs

            cls = _Cooldown
        else:
            cls = None

        return cls

    @property
    def has_cooldown(self):
        has_cooldown = self.cooldown_class is not None and self.cooldown_class().has_cooldown()
        return has_cooldown

    def reset_cooldown(self):
        if self.cooldown_class:
            was_reset = self.cooldown_class().reset_cooldown(force=self.force_cooldown)
        else:
            was_reset = False

        return was_reset

    def __call__(self, task_fn):
        @shared_task
        @wraps(task_fn)
        def wrapped(*args, **kwargs):
            try:
                slack_notifications_enabled = self.notify and htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED')
                if slack_notifications_enabled:
                    slack_notify('Processing *%s*...' % self.task_name)

                timer = HtkTimer()
                timer.start()

                was_skipped = False

                if self.has_cooldown:
                    # this task has a cooldown to prevent running too frequently
                    # do nothing
                    was_skipped = True
                else:
                    result = task_fn(*args, **kwargs)
                    # reset cooldown to prevent future jobs from running too soon
                    self.reset_cooldown()

                timer.stop()

                if slack_notifications_enabled:
                    duration = timer.duration()
                    skipped_msg = '(SKIPPED) ' if was_skipped else ''
                    msg = '%sFinished processing *%s* in *%s* seconds %s' % (skipped_msg, self.task_name, duration,)
                    slack_notify(msg)
            except:
                result = None
                extra_data = {
                    'task_name' : self.task_name,
                }
                rollbar.report_exc_info(extra_data=extra_data)
            finally:
                return result
        return wrapped
