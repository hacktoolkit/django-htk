# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.contrib.sites.models import Site
from django.db import models

# HTK Imports
from htk.apps.prelaunch.emails import prelaunch_email
from htk.utils import (
    htk_setting,
    utcnow,
)
from htk.utils.request import get_current_request


# isort: off

class PrelaunchSignup(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=128, blank=True)
    email = models.EmailField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'htk'
        verbose_name = 'Prelaunch Signup'

    def __str__(self):
        s = '%s - %s' % (self.created_on, self.email,)
        return s

    def send_notifications(self):
        if htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED'):
            from htk.utils.notifications import slack_notify
            try:
                message = '{} <{}> just signed up for the pre-launch waiting list.'.format(
                    self.full_name,
                    self.email
                )
                slack_notify(message)
            except:
                request = get_current_request()
                rollbar.report_exc_info(request=request)
        else:
            pass

        try:
            prelaunch_email(self)
        except Exception:
            request = get_current_request()
            rollbar.report_exc_info(request=request)
