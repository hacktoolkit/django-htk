# Python Standard Library Imports
import uuid

# Third Party (PyPI) Imports
import rollbar
from baws.utils.urls import get_full_url

# Django Imports
from django.contrib.sites.models import Site
from django.db import models

# HTK Imports
from htk.apps.prelaunch.emails import (
    early_access_email,
    prelaunch_email,
)
from htk.utils import htk_setting
from htk.utils.notifications import notify
from htk.utils.request import get_current_request


# isort: off


class BasePrelaunchSignup(models.Model):
    site = models.ForeignKey(
        Site,
        related_name='prelaunch_signups',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    email = models.EmailField(null=True, blank=True)
    early_access = models.BooleanField(default=False)
    early_access_code = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        s = '%s - %s' % (
            self.email,
            self.created_at,
        )
        return s

    @classmethod
    def get_or_create_by_email(
        cls,
        email,
        first_name='',
        last_name='',
        site=None,
        enable_early_access=False,
    ):
        """Gets or creates a `PrelaunchSignup` object by `email` and `site`

        If `enable_early_access` is `True`, will also enable for early access.
        """
        try:
            prelaunch_signups = cls.objects.filter(email=email, site=site)
            prelaunch_signups_with_early_access = prelaunch_signups.filter(
                early_access=True
            )
            prelaunch_signup = (
                prelaunch_signups_with_early_access.first()
                or prelaunch_signups.first()
            )

            should_update = False
            was_updated = False

            # update existing details
            if prelaunch_signup.first_name != first_name:
                prelaunch_signup.first_name = first_name
                should_update = True

            if prelaunch_signup.last_name != last_name:
                prelaunch_signup.last_name = last_name
                should_update = True

            if enable_early_access and not prelaunch_signup.early_access:
                prelaunch_signup.grant_early_access()
                was_updated = True

            if should_update and not was_updated:
                prelaunch_signup.save()

        except cls.DoesNotExist:
            prelaunch_signup = cls(
                first_name=first_name,
                last_name=last_name,
                email=email,
                site=site,
            )
            if enable_early_access:
                # granting early access will also save the object
                prelaunch_signup.grant_early_access()
            else:
                # explicitly save the object if not granting early access
                prelaunch_signup.save()

        return prelaunch_signup

    @property
    def full_name(self):
        separator = (
            ' ' if self.first_name.strip() and self.last_name.strip() else ''
        )
        full_name = '{}{}{}'.format(
            self.first_name.strip(),
            separator,
            self.last_name.strip(),
        )
        return full_name

    @property
    def notification_message(self):
        """Returns a message for Slack notifications about platform activity

        NOTE: This is a template method that should be overridden in subclasses
        """
        message = (
            '{} <{}> just signed up for the pre-launch waiting list.'.format(
                self.full_name,
                self.email,
            )
        )
        return message

    def send_notifications(self):
        if htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED'):
            from htk.utils.notifications import slack_notify

            try:
                slack_notify(self.notification_message)
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
        notify(
            'Early access has been enabled for {} <{}>'.format(
                self.full_name, self.email
            ),
            level='info',
        )

        try:
            early_access_email(self)
        except Exception:
            request = get_current_request()
            rollbar.report_exc_info(request=request)

    def revoke_early_access(self):
        self.early_access = False
        self.early_access_code = None
        self.save()

    @property
    def early_access_url(self):
        if self.early_access:
            early_access_url = '{}?early_access_code={}'.format(
                get_full_url('/'),
                self.early_access_code,
            )
        else:
            early_access_url = None

        return early_access_url
