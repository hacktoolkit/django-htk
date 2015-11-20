from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from htk.apps.cpq.constants import *
from htk.apps.cpq.utils import compute_cpq_code
from htk.fields import CurrencyField
from htk.utils.enums import enum_to_str

class BaseCPQQuote(models.Model):
    """Base class for a Quote
    Quote has not been executed yet (signed or paid)
    Once executed, an invoice is generated
    """
    # related_name = customer.quotes, customer.invoices
    customer = models.ForeignKey(settings.HTK_CPQ_CUSTOMER_MODEL, related_name='%(class)ss')
    date = models.DateField()
    notes = models.TextField(max_length=1024, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        value = 'CPQ #%s' % self.id
        return value

    def get_encoded_id(self):
        invoice_code = compute_cpq_code(self)
        return invoice_code

    def get_url_name(self):
        """Gets the url_name for this object
        Abstract method must be overrided
        """
        raise Exception('get_url_name abstract method not implemented')

    def get_url(self):
        url_name = self.get_url_name()
        url = reverse(url_name, args=(self.get_encoded_id(),))
        return url

    def get_total(self):
        line_items = self.line_items.all()
        subtotal = 0
        for line_item in line_items:
            subtotal += line_item.get_amount()
        return subtotal

class BaseCPQInvoice(BaseCPQQuote):
    """Base class for an Invoice
    """
    invoice_type = models.PositiveIntegerField(default=HTK_CPQ_INVOICE_DEFAULT_TYPE.value)
    paid = models.BooleanField(default=False)
    payment_terms = models.PositiveIntegerField(default=HTK_CPQ_INVOICE_DEFAULT_PAYMENT_TERM.value)

    class Meta:
        abstract = True

    def __unicode__(self):
        value = 'Invoice #%s' % self.id
        return value

    def get_url_name(self):
        url_name = 'invoices_invoice'
        return url_name

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

class BaseCPQQuoteLineItem(BaseCPQLineItem):
    quote = models.ForeignKey(settings.HTK_CPQ_QUOTE_MODEL, related_name = 'line_items')

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
