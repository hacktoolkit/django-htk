from django.conf import settings
from django.db import models

class BaseCustomer(models.Model):
    name = models.CharField(max_length=64)
    attention = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True)
    address = models.ForeignKey(settings.HTK_POSTAL_ADDRESS_MODEL, related_name='customers')

    class Meta:
        abstract = True

    def __unicode__(self):
        value = 'Customer %s: %s' % (self.id, self.name,)
        return value
