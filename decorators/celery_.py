# Python Standard Library Imports
from functools import wraps

# Third Party (PyPI) Imports
import rollbar
from celery import shared_task

# HTK Imports
from htk.utils import htk_setting
from htk.utils.notifications import slack_notify
from htk.utils.timer import HtkTimer


class safe_timed_task(object):
    def __init__(self, task_name, notify=False):
        self.task_name = task_name
        self.notify = notify

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
                result = task_fn(*args, **kwargs)
                timer.stop()

                if slack_notifications_enabled:
                    duration = timer.duration()
                    msg = 'Finished processing *%s* in *%s* seconds' % (self.task_name, duration,)
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
