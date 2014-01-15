import datetime

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models

class Feedback(models.Model):
    site = models.ForeignKey(Site)
    user = models.ForeignKey(User, related_name='feedback', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    comment = models.CharField(max_length=2000, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    uri = models.CharField(max_length=200, null=True, blank=True)
    processed = models.BooleanField(default=False)
    needs_followup = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        app_label = 'htk'
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'

    def __unicode__(self):
        s = '%s, %s, [%s]' % (
            self.date_created.strftime('%Y-%m-%d %H:%M:%S'),
            self.uri,
            self.comment[:50] + '...' if len(self.comment) > 50 else self.comment
        )
        return s
