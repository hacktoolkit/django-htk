from django.contrib.sites.models import Site
from django.db import models

from htk.utils import utcnow

class PrelaunchSignup(models.Model):
    site = models.ForeignKey(Site)
    email = models.EmailField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, default=utcnow)

    class Meta:
        app_label = 'htk'
        verbose_name = 'Prelaunch Signup'

    def __unicode__(self):
        s = '%s - %s' % (self.created_on, self.email,)
        return s
