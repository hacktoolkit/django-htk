from django.conf import settings
from django.db import models

from htk.models import AbstractAttribute
from htk.models import AbstractAttributeHolderClassFactory
from htk.utils import htk_setting

class CustomerAttribute(AbstractAttribute):
    holder = models.ForeignKey(htk_setting('HTK_CPQ_CUSTOMER_MODEL'), related_name='attributes')

    class Meta:
        app_label = htk_setting('HTK_DEFAULT_APP_LABEL')
        verbose_name = 'Customer Attribute'
        unique_together = (
            ('holder', 'key',),
        )

    def __unicode__(self):
        value = '%s (%s)' % (self.key, self.holder)
        return value

CustomerAttributeHolder = AbstractAttributeHolderClassFactory(
    CustomerAttribute
).get_class()

class BaseCustomer(models.Model, CustomerAttributeHolder):
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
