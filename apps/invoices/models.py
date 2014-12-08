from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from htk.apps.invoices.constants import *
from htk.apps.invoices.utils import compute_invoice_code
from htk.fields import CurrencyField
from htk.utils.enums import enum_to_str

class BaseInvoice(models.Model):
    customer = models.ForeignKey(settings.HTK_INVOICE_CUSTOMER_MODEL, related_name='invoices')
    date = models.DateField()
    notes = models.TextField(max_length=256, blank=True)
    invoice_type = models.PositiveIntegerField(default=HTK_INVOICE_DEFAULT_TYPE.value)
    paid = models.BooleanField(default=False)
    payment_terms = models.PositiveIntegerField(default=HTK_INVOICE_DEFAULT_PAYMENT_TERM.value)

    class Meta:
        abstract = True

    def __unicode__(self):
        value = 'Invoice #%s' % self.id
        return value

    def get_encoded_id(self):
        invoice_code = compute_invoice_code(self)
        return invoice_code

    def get_url(self):
        url = reverse('invoices_invoice', args=(self.get_encoded_id(),))
        return url

    def get_total(self):
        line_items = self.line_items.all()
        subtotal = 0
        for line_item in line_items:
            subtotal += line_item.get_amount()
        return subtotal

    def get_invoice_type(self):
        from htk.apps.invoices.enums import InvoiceType
        invoice_type = InvoiceType(self.invoice_type)
        return invoice_type

    def get_payment_terms(self):
        from htk.apps.invoices.enums import InvoicePaymentTerm
        invoice_payment_term = InvoicePaymentTerm(self.payment_terms)
        str_value = enum_to_str(invoice_payment_term)
        return str_value

class BaseInvoiceLineItem(models.Model):
    invoice = models.ForeignKey(settings.HTK_INVOICE_MODEL, related_name='line_items')
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=256)
    unit_cost = CurrencyField(default=0)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        abstract = True

    def __unicode__(self):
        value = 'Line Item for Invoice #%s' % self.invoice.id
        return value

    def get_amount(self):
        amount = self.unit_cost * self.quantity
        return amount
