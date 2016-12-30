from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models

from htk.models import HtkBaseModel
from htk.utils import utcnow

class Feedback(HtkBaseModel):
    site = models.ForeignKey(Site)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='feedback', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    comment = models.CharField(max_length=2000, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    uri = models.CharField(max_length=200, null=True, blank=True)
    # admin
    processed = models.BooleanField(default=False)
    needs_followup = models.BooleanField(default=True)
    # read-only
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'htk'
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'

    def __unicode__(self):
        s = '%s, %s, [%s]' % (
            self.created_on.strftime('%Y-%m-%d %H:%M:%S'),
            self.uri,
            self.comment[:50] + '...' if len(self.comment) > 50 else self.comment
        )
        return s
