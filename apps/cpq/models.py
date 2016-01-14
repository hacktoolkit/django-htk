from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from htk.apps.cpq.constants import *
from htk.apps.cpq.utils import compute_cpq_code
from htk.fields import CurrencyField
from htk.utils.enums import enum_to_str
from htk.utils import htk_setting

class AbstractCPQQuote(models.Model):
    """Abstract base class for a Quote, Invoice, or GroupQuote
    """
    date = models.DateField()
    notes = models.TextField(max_length=1024, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        value = 'CPQ #%s' % self.id
        return value

    def get_type(self):
        return 'Quote'

    def get_encoded_id(self):
        invoice_code = compute_cpq_code(self)
        return invoice_code

    def get_url_name(self):
        """Gets the url_name for this object
        Abstract method must be overridden
        """
        raise Exception('get_url_name abstract method not implemented')

    def get_url(self):
        url_name = self.get_url_name()
        url = reverse(url_name, args=(self.get_encoded_id(),))
        return url

    def get_full_url(self, base_uri=None):
        if base_uri is None:
            domain = htk_setting('HTK_DEFAULT_DOMAIN')
            base_uri = 'http://%s' % domain
        cpq_url = self.get_url()
        full_url = '%s%s' % (base_uri, cpq_url,)
        return full_url

    def get_total(self):
        line_items = self.line_items.all()
        subtotal = 0
        for line_item in line_items:
            subtotal += line_item.get_amount()
        return subtotal

class BaseCPQQuote(AbstractCPQQuote):
    """Base class for a Quote

    Quote has not been executed yet (signed or paid)
    """
    customer = models.ForeignKey(settings.HTK_CPQ_CUSTOMER_MODEL, related_name='%(class)ss')
    group_quote = models.ForeignKey(settings.HTK_CPQ_GROUP_QUOTE_MODEL, null=True, blank=True, default=None, related_name='%(class)ss')

    class Meta:
        abstract = True

    def get_url_name(self):
        url_name = 'cpq_quotes_quote'
        return url_name

class BaseCPQGroupQuote(AbstractCPQQuote):
    """Base class for a GroupQuote

    A GroupQuote's details serves as the lookup for many individual Quotes in the group (OrganizationCustomer)
    """
    organization = models.ForeignKey(htk_setting('HTK_CPQ_ORGANIZATION_CUSTOMER_MODEL'), related_name='member_%(class)ss')

    class Meta:
        abstract = True

    def customer(self):
        return self.organization

    def get_url_name(self):
        url_name = 'cpq_groupquotes_quote'
        return url_name

class BaseCPQInvoice(AbstractCPQQuote):
    """Base class for an Invoice

    An Invoice can be standalone, or get generated when its corresponding Quote is executed
    """
    customer = models.ForeignKey(settings.HTK_CPQ_CUSTOMER_MODEL, related_name='%(class)ss')
    invoice_type = models.PositiveIntegerField(default=HTK_CPQ_INVOICE_DEFAULT_TYPE.value)
    paid = models.BooleanField(default=False)
    payment_terms = models.PositiveIntegerField(default=HTK_CPQ_INVOICE_DEFAULT_PAYMENT_TERM.value)
    quote = models.ForeignKey(settings.HTK_CPQ_QUOTE_MODEL, null=True, blank=True, default=None, on_delete=models.SET_DEFAULT, related_name='%(class)ss')

    class Meta:
        abstract = True

    def __unicode__(self):
        value = 'Invoice #%s' % self.id
        return value

    def get_url_name(self):
        url_name = 'cpq_invoices_invoice'
        return url_name

    def get_type(self):
        return self.get_invoice_type()

    def get_invoice_type(self):
        from htk.apps.cpq.enums import InvoiceType
        invoice_type = InvoiceType(self.invoice_type)
        str_value = enum_to_str(invoice_type)
        return str_value

    def get_payment_terms(self):
        from htk.apps.cpq.enums import InvoicePaymentTerm
        invoice_payment_term = InvoicePaymentTerm(self.payment_terms)
        str_value = enum_to_str(invoice_payment_term)
        return str_value

class BaseCPQLineItem(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=256)
    unit_cost = CurrencyField(default=0)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        abstract = True

    def get_amount(self):
        amount = self.unit_cost * self.quantity
        return amount

class BaseCPQGroupQuoteLineItem(BaseCPQLineItem):
    group_quote = models.ForeignKey(settings.HTK_CPQ_GROUP_QUOTE_MODEL, related_name='line_items')

    class Meta:
        abstract = True

    def __unicode__(self):
        value = 'Line Item for %s #%s' % (self.__class__.__name__, self.group_quote.id,)
        return value

class BaseCPQQuoteLineItem(BaseCPQLineItem):
    quote = models.ForeignKey(settings.HTK_CPQ_QUOTE_MODEL, related_name='line_items')

    class Meta:
        abstract = True

    def __unicode__(self):
        value = 'Line Item for %s #%s' % (self.__class__.__name__, self.quote.id,)
        return value

class BaseCPQInvoiceLineItem(BaseCPQLineItem):
    invoice = models.ForeignKey(settings.HTK_CPQ_INVOICE_MODEL, related_name='line_items')

    class Meta:
        abstract = True

    def __unicode__(self):
        value = 'Line Item for %s #%s' % (self.__class__.__name__, self.invoice.id,)
        return value
