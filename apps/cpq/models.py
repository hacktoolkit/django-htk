# Python Standard Library Imports
import json

# Django Imports
from django.conf import settings
from django.db import models
from django.urls import reverse

# HTK Imports
from htk.apps.cpq.constants import *
from htk.apps.cpq.utils import compute_cpq_code
from htk.apps.cpq.utils.general import get_invoice_payment_terms_choices
from htk.fields import CurrencyField
from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically
from htk.utils import utcnow
from htk.utils.cache_descriptors import CachedAttribute
from htk.utils.enums import enum_to_str


class AbstractCPQQuote(models.Model):
    """Abstract base class for a Quote, Invoice, or GroupQuote
    """
    date = models.DateField()
    notes = models.TextField(max_length=1024, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
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

    def get_payment_uri(self):
        uri = ''
        return uri

    def get_notes(self):
        notes = self.notes
        return notes

    def get_line_items(self):
        line_items = self.line_items.all()
        return line_items

    def get_total(self):
        line_items = self.get_line_items()
        subtotal = 0
        for line_item in line_items:
            subtotal += line_item.get_amount()
        return subtotal


class BaseCPQQuote(AbstractCPQQuote):
    """Base class for a Quote

    Quote has not been executed yet (signed or paid)
    """
    customer = models.ForeignKey(settings.HTK_CPQ_CUSTOMER_MODEL, related_name='%(class)ss', on_delete=models.CASCADE)
    group_quote = models.ForeignKey(settings.HTK_CPQ_GROUP_QUOTE_MODEL, null=True, blank=True, default=None, related_name='%(class)ss', on_delete=models.SET_DEFAULT)

    class Meta:
        abstract = True

    def use_group_quote(self):
        _use_group_quote = self.group_quote and not self.line_items.exists()
        return _use_group_quote

    def get_notes(self):
        if self.use_group_quote():
            notes = self.group_quote.get_notes()
        else:
            notes = self.notes
        return notes

    def get_line_items(self):
        if self.use_group_quote():
            line_items = self.group_quote.get_line_items()
        else:
            line_items = self.line_items.all()
        return line_items

    def get_url_name(self):
        url_name = 'cpq_quotes_quote'
        return url_name

    def get_payment_uri(self):
        uri = reverse('cpq_quotes_quote_pay', args=(self.get_encoded_id(),))
        return uri

    def get_payments(self):
        payments = filter(bool, [invoice.get_payment() for invoice in self.invoices.all()])
        return payments

    def resolve_line_item_ids(self, line_item_ids, strict=True):
        """Resolves `line_item_ids` into their respective GroupQuoteLineItems or QuoteLineItems
        If `strict`, require all ids to be resolveable
        """
        if self.group_quote:
            line_items = self.group_quote.line_items.filter(id__in=line_item_ids)
        else:
            line_items = self.line_items.filter(id__in=line_item_ids)
        line_items = line_items.order_by('id')
        if strict and line_items.count() != len(line_item_ids):
            raise Exception('Could not resolve all line item ids')
        return line_items

    def approve_and_pay(self, stripe_token, amount, email, line_item_ids):
        """Approve `line_item_ids` and pay `amount` for them with a verified `stripe_token`
        """
        success = False
        amount = int(amount)
        description = '%s %s: %s' % (
            htk_setting('HTK_SITE_NAME'),
            self.get_type(),
            self.id,
        )
        # HTK Imports
        from htk.lib.stripe_lib.utils import create_customer
        customer, stripe_customer = create_customer(
            stripe_token,
            email=email,
            description=description
        )
        line_items = self.resolve_line_item_ids(line_item_ids)
        metadata = {
            'quote' : self.id,
            'line_item_ids' : ','.join(line_item_ids),
            'line_items' : ','.join(['[%s] %s' % (line_item.id, line_item.name,) for line_item in line_items]),
        }
        success = customer.charge(amount=amount, metadata=metadata)
        if success:
            self.create_invoice_for_payment(customer, line_items)
        # TODO: send the customer an email receipt
        return success

    def create_invoice_for_payment(self, stripe_customer, line_items):
        """Creates an invoice for this Quote with successful payment by `stripe_customer` for `line_items`
        """
        InvoiceModel = resolve_model_dynamically(htk_setting('HTK_CPQ_INVOICE_MODEL'))
        invoice = InvoiceModel.objects.create(
            date=utcnow(),
            customer=self.customer,
            paid=True,
            quote=self
        )
        invoice.record_payment(stripe_customer, line_items)

    @CachedAttribute
    def amount_paid(self):
        subtotal = 0
        for invoice in self.invoices.filter(paid=True):
            subtotal += invoice.get_total()
        return subtotal

    @CachedAttribute
    def payment_status(self):
        amount_paid = self.amount_paid
        total = self.get_total()
        if amount_paid == 0:
            status = 'Not Paid'
        elif amount_paid < total:
            status = 'Partially Paid'
        else:
            status = 'Paid in Full'
        return status


class BaseCPQGroupQuote(AbstractCPQQuote):
    """Base class for a GroupQuote

    A GroupQuote's details serves as the lookup for many individual Quotes in the group (OrganizationCustomer)
    """
    organization = models.ForeignKey(htk_setting('HTK_CPQ_ORGANIZATION_CUSTOMER_MODEL'), related_name='member_%(class)ss', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        value = 'Group Quote #%s - %s' % (self.id, self.organization.name,)
        return value

    def customer(self):
        return self.organization

    def get_url_name(self):
        url_name = 'cpq_groupquotes_quote'
        return url_name

    def get_all_quotes_url(self):
        url_name = 'cpq_groupquotes_quote_all'
        url = reverse(url_name, args=(self.get_encoded_id(),))
        return url


class BaseCPQInvoice(AbstractCPQQuote):
    """Base class for an Invoice

    An Invoice can be standalone, or get generated when its corresponding Quote is executed
    """
    customer = models.ForeignKey(settings.HTK_CPQ_CUSTOMER_MODEL, related_name='%(class)ss', on_delete=models.CASCADE)
    invoice_type = models.PositiveIntegerField(default=HTK_CPQ_INVOICE_DEFAULT_TYPE.value)
    paid = models.BooleanField(default=False)
    payment_terms = models.PositiveIntegerField(default=HTK_CPQ_INVOICE_DEFAULT_PAYMENT_TERM.value, choices=get_invoice_payment_terms_choices())
    quote = models.ForeignKey(settings.HTK_CPQ_QUOTE_MODEL, null=True, blank=True, default=None, on_delete=models.SET_DEFAULT, related_name='%(class)ss')

    class Meta:
        abstract = True

    def __str__(self):
        value = 'Invoice #%s' % self.id
        return value

    def get_url_name(self):
        url_name = 'cpq_invoices_invoice'
        return url_name

    def get_type(self):
        return self.get_invoice_type()

    def get_invoice_type(self):
        # HTK Imports
        from htk.apps.cpq.enums import InvoiceType
        invoice_type = InvoiceType(self.invoice_type)
        str_value = enum_to_str(invoice_type)
        return str_value

    def get_payment_terms(self):
        # HTK Imports
        from htk.apps.cpq.enums import InvoicePaymentTerm
        invoice_payment_term = InvoicePaymentTerm(self.payment_terms)
        str_value = enum_to_str(invoice_payment_term)
        return str_value

    ##
    # payment tracking

    def get_payment_key(self):
        key = 'invoice_%s_payment' % self.id
        return key

    def get_payment(self):
        key = self.get_payment_key()
        payment = self.customer.get_attribute(key)
        payment = json.loads(payment) if payment else None
        return payment

    def record_payment(self, stripe_customer, line_items):
        """Record an actual Stripe payment for `line_items`
        Also creates InvoiceLineItems on this Invoice

        `line_items` are either GroupQuoteLineItems or QuoteLineItems

        Note: this function should only be called once for any Invoice
        """
        for line_item in line_items:
            self.line_items.create(
                name=line_item.name,
                description=line_item.description,
                unit_cost=line_item.unit_cost,
                quantity=line_item.quantity
            )
        key = self.get_payment_key()
        payment = {
            'stripe_customer' : stripe_customer.id,
            'invoice' : self.id,
        }
        if len(line_items) and hasattr(line_items[0], 'quote'):
            payment['quote_line_item_ids'] = [line_item.id for line_item in line_items]
        self.customer.set_attribute(key, json.dumps(payment))

    def get_charges(self):
        """Get charges made on this Invoice
        """
        payment = self.get_payment()
        if payment:
            stripe_customer_id = payment['stripe_customer']
            StripeCustomerModel = resolve_model_dynamically(htk_setting('HTK_STRIPE_CUSTOMER_MODEL'))
            stripe_customer = StripeCustomerModel.objects.get(id=stripe_customer_id)
            charges = stripe_customer.get_charges()
        else:
            charges = None
        return charges


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
    group_quote = models.ForeignKey(settings.HTK_CPQ_GROUP_QUOTE_MODEL, related_name='line_items', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        value = 'Line Item for %s #%s' % (self.__class__.__name__, self.group_quote.id,)
        return value


class BaseCPQQuoteLineItem(BaseCPQLineItem):
    quote = models.ForeignKey(settings.HTK_CPQ_QUOTE_MODEL, related_name='line_items', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        value = 'Line Item for %s #%s' % (self.__class__.__name__, self.quote.id,)
        return value


class BaseCPQInvoiceLineItem(BaseCPQLineItem):
    invoice = models.ForeignKey(settings.HTK_CPQ_INVOICE_MODEL, related_name='line_items', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        value = 'Line Item for %s #%s' % (self.__class__.__name__, self.invoice.id,)
        return value
