# Django Imports
from django.conf import settings
from django.db import models
from django.urls import reverse

# HTK Imports
from htk.apps.customers.constants import *
from htk.apps.customers.utils import get_organization_type_choices
from htk.lib.stripe_lib.models import AbstractStripeCustomerHolder
from htk.models import AbstractAttribute
from htk.models import AbstractAttributeHolderClassFactory
from htk.utils import htk_setting
from htk.utils.cache_descriptors import CachedAttribute


class CustomerAttribute(AbstractAttribute):
    holder = models.ForeignKey(htk_setting('HTK_CPQ_CUSTOMER_MODEL'), related_name='attributes')

    class Meta:
        app_label = htk_setting('HTK_DEFAULT_APP_LABEL')
        verbose_name = 'Customer Attribute'
        unique_together = (
            ('holder', 'key',),
        )

    def __str__(self):
        value = '%s (%s)' % (self.key, self.holder)
        return value

CustomerAttributeHolder = AbstractAttributeHolderClassFactory(
    CustomerAttribute
).get_class()

class OrganizationCustomerAttribute(AbstractAttribute):
    holder = models.ForeignKey(htk_setting('HTK_CPQ_ORGANIZATION_CUSTOMER_MODEL'), related_name='attributes')

    class Meta:
        app_label = htk_setting('HTK_DEFAULT_APP_LABEL')
        verbose_name = 'Organization Customer Attribute'
        unique_together = (
            ('holder', 'key',),
        )

    def __str__(self):
        value = '%s (%s)' % (self.key, self.holder)
        return value

OrganizationCustomerAttributeHolder = AbstractAttributeHolderClassFactory(
    OrganizationCustomerAttribute
).get_class()

class BaseCustomer(models.Model, CustomerAttributeHolder):
    """Base model for a Customer in the `htk.apps.cpq` app
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customers', null=True, blank=True)
    name = models.CharField(max_length=64, default='Customer Name')
    attention = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True)
    address = models.ForeignKey(settings.HTK_POSTAL_ADDRESS_MODEL, related_name='customers')
    mailing_address = models.ForeignKey(settings.HTK_POSTAL_ADDRESS_MODEL, related_name='mailing_address_customers', null=True, blank=True)
    organization = models.ForeignKey(htk_setting('HTK_CPQ_ORGANIZATION_CUSTOMER_MODEL'), related_name='members', null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = 'Customer'

    def __str__(self):
        value = 'Customer %s: %s' % (self.id, self.name,)
        return value

class BaseOrganizationCustomer(models.Model):
    """Base model for an OrganizationCustomer in the `htk.apps.cpq` app

    OrganizationCustomers allow for multiple Customers to be `members` under one Organization.
    Valid organization types are specified by the enum OrganizationType
    Examples:
    - Companies
    - HOAs

    Depending on additional rules, constituents (`members`) can share or have separate billing accounts, or have group or individual Quotes or Invoices
    """
    name = models.CharField(max_length=64, default='Organization Customer Name')
    attention = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True)
    address = models.ForeignKey(settings.HTK_POSTAL_ADDRESS_MODEL, related_name='organization_customers', editable=True)
    mailing_address = models.ForeignKey(settings.HTK_POSTAL_ADDRESS_MODEL, related_name='mailing_address_organization_customers', null=True, blank=True)
    organization_type = models.PositiveIntegerField(default=DEFAULT_ORGANIZATION_TYPE.value, choices=get_organization_type_choices())

    class Meta:
        abstract = True
        verbose_name = 'Organization Customer'

    def __str__(self):
        value = 'Organization Customer %s: %s' % (self.id, self.name,)
        return value

    @CachedAttribute
    def members_changelist_url(self):
        app_label = htk_setting('HTK_DEFAULT_APP_LABEL')
        members_changelist_url = '%s?organization__id__exact=%s' % (
            reverse('admin:%s_%s_changelist' % (app_label, 'customer',)),
            self.id,
        )
        return members_changelist_url
