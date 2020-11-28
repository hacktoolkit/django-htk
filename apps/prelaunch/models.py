# Django Imports
from django.contrib.sites.models import Site
from django.db import models

# HTK Imports
from htk.utils import utcnow


class PrelaunchSignup(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'htk'
        verbose_name = 'Prelaunch Signup'

    def __str__(self):
        s = '%s - %s' % (self.created_on, self.email,)
        return s
