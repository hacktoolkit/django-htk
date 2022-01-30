# Python Standard Library Imports
import uuid

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
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    email = models.EmailField(null=True, blank=True)
    early_access = models.BooleanField(default=False)
    early_access_code = models.CharField(max_length=64, unique=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'htk'
        verbose_name = 'Prelaunch Signup'

    def __str__(self):
        s = '%s - %s' % (self.created_on, self.email,)
        return s

    @property
    def full_name(self):
        separator = ' ' if self.first_name.strip() and self.last_name.strip() else ''
        full_name = '{}{}{}'.format(
            self.first_name.strip(),
            separator,
            self.last_name.strip()
        )
        return full_name

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

    def toggle_early_access(self):
        if self.early_access:
            self.revoke_early_access()
        else:
            self.grant_early_access()

    def grant_early_access(self):
        self.early_access = True
        self.early_access_code = uuid.uuid4().hex
        self.save()

    def revoke_early_access(self):
        self.early_access = False
        self.early_access_code = None
        self.save()
