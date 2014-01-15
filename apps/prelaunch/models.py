import datetime

from django.contrib.sites.models import Site
from django.db import models

class PrelaunchSignup(models.Model):
    site = models.ForeignKey(Site)
    email = models.EmailField(null=True, blank=True)
    date_created = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        app_label = 'htk'
        verbose_name = 'Prelaunch Signup'

    def __unicode__(self):
        s = '%s - %s' % (self.date_created, self.email,)
        return s
