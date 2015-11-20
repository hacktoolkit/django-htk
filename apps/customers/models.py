from django.conf import settings
from django.db import models

class BaseCustomer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customers', null=True, blank=True)
    name = models.CharField(max_length=64)
    attention = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True)
    address = models.ForeignKey(settings.HTK_POSTAL_ADDRESS_MODEL, related_name='customers')
    mailing_address = models.ForeignKey(settings.HTK_POSTAL_ADDRESS_MODEL, related_name='mailing_address_customers', null=True, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        value = 'Customer %s: %s' % (self.id, self.name,)
        return value
