# Python Standard Library Imports

# Third Party (PyPI) Imports
import rollbar
import stripe

# Django Imports
from django.conf import settings
from django.db import models

# HTK Imports
from htk.lib.stripe_lib.constants.general import *
from htk.lib.stripe_lib.enums import (
    StripePlanInterval,
    StripeProductType,
)
from htk.lib.stripe_lib.utils import (
    _initialize_stripe,
    safe_stripe_call,
)
from htk.utils import htk_setting
from htk.utils.request import get_current_request


class BaseStripeModel(models.Model):
    # class attributes
    STRIPE_API_CLASS = None

    # fields
    stripe_id = models.CharField(max_length=255)
    live_mode = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        value = '%s - %s (%s)' % (
            self.__class__.__name__,
            self.stripe_id,
            self.mode_str,
        )
        return value

    @property
    def mode_str(self):
        mode_str = 'Live' if self.live_mode else 'Test'
        return mode_str

    def retrieve(self):
        """Retrieves a Stripe object via API

        - https://stripe.com/docs/api/customers/retrieve
        - https://stripe.com/docs/api/products/retrieve
        - https://stripe.com/docs/api/prices/retrieve
        - https://stripe.com/docs/api/plans/retrieve
        """
        _initialize_stripe(live_mode=self.live_mode)
        args = (
            self.stripe_id,
        )
        stripe_obj = safe_stripe_call(self.STRIPE_API_CLASS.retrieve, *args)
        return stripe_obj


class BaseStripeCustomer(BaseStripeModel):
    """Django model for Stripe Customer

    See: https://stripe.com/docs/api/customers
    """
    # class attributes
    STRIPE_API_CLASS = stripe.Customer

    class Meta:
        abstract = True

    ##
    # customer details

    def modify(self, **kwargs):
        """Updates the customer

        https://stripe.com/docs/api/customers/update
        """
        _initialize_stripe(live_mode=self.live_mode)
        args = (
            self.stripe_id,
        )
        cu = safe_stripe_call(
            self.STRIPE_API_CLASS.modify,
            *args,
            **kwargs
        )
        return cu

    def update_email(self, email=None):
        """Updates the email for this Customer
        """
        stripe_customer = None
        if email is not None:
            stripe_customer = self.retrieve()
            if stripe_customer['email'] != email:
                kwargs = {
                    'email': email,
                }
                self.modify(**kwargs)
            else:
                pass
        else:
            pass
        return stripe_customer

    ##
    # payments

    def charge(self, amount=0, currency=DEFAULT_STRIPE_CURRENCY, metadata=None):
        """Charges a Customer

        https://stripe.com/docs/api/charges/create
        """
        if metadata is None:
            metadata = {}

        _initialize_stripe(live_mode=self.live_mode)
        stripe_charge = safe_stripe_call(
            stripe.Charge.create,
            **{
                'amount': amount,
                'currency': currency,
                'customer': self.stripe_id,
                'metadata': metadata,
            }
        )
        return stripe_charge

    def get_charges(self):
        """List charges for a customer

        https://stripe.com/docs/api/charges/list
        """
        _initialize_stripe(live_mode=self.live_mode)
        stripe_charges = safe_stripe_call(
            stripe.Charge.list,
            **{
                'customer': self.stripe_id,
            }
        )
        charges = charges.get('data')
        return charges

    def add_invoice_item(self, stripe_price_id, quantity=None):
        """Create an `InvoiceItem` for the `Customer`

        https://stripe.com/docs/api/invoiceitems/create?lang=python
        """
        _initialize_stripe(live_mode=self.live_mode)

        kwargs = {
            'customer': self.stripe_id,
            'price': stripe_price_id,
        }

        if quantity is not None:
            kwargs['quantity'] = quantity

        stripe_invoice_item = safe_stripe_call(
            stripe.InvoiceItem.create,
            **kwargs
        )
        return stripe_invoice_item

    def create_invoice(self):
        """Create an Invoice for this Customer to pay any outstanding invoice items such as when upgrading plans

        https://stripe.com/docs/api/invoices/create
        """
        _initialize_stripe(live_mode=self.live_mode)
        stripe_invoice = safe_stripe_call(
            stripe.Invoice.create,
            **{
                'customer': self.stripe_id,
            }
        )

        if stripe_invoice is None:
            rollbar.report_message('Could not create invoice for Customer %s' % self.stripe_id, 'error')
        else:
            pass

        return stripe_invoice

    def create_invoice_and_pay(self):
        """
        After creating the Invoice, have the Customer immediately pay it

        https://stripe.com/docs/api/invoices/pay
        """
        stripe_invoice = self.create_invoice()
        if stripe_invoice:
            args = (
                stripe_invoice['id'],
            )
            result = safe_stripe_call(stripe.Invoice.pay, *args)
        else:
            # invoice not created, do nothing
            result = stripe_invoice

        return result

    ##
    # cards

    def add_card(self, card):
        """Add an additional credit card to the customer

        https://stripe.com/docs/api/cards/create
        """
        args = (
            self.stripe_id,
        )
        kwargs = {
            'source': card,
        }
        stripe_card = safe_stripe_call(
            self.STRIPE_API_CLASS.create_source,
            *args,
            **kwargs
        )

        return stripe_card

    def retrieve_card(self, card_id):
        """Retrieves a card

        https://stripe.com/docs/api/cards/retrieve
        """
        args = (
            self.stripe_id,
            card_id,
        )
        stripe_card = safe_stripe_call(
            self.STRIPE_API_CLASS.retrieve_source,
            *args
        )
        return stripe_card

    def replace_card(self, card):
        """Adds a new credit card and sets it as this Customer's default source

        See:
        - https://stripe.com/docs/api/cards/create
        - https://stripe.com/docs/api/cards/update
        - https://stripe.com/docs/api/customers/update
        """
        # first, add the card
        stripe_card = self.add_card(card)

        if stripe_card:
            kwargs = {
                'default_source': stripe_card['id'],
            }
            cu = self.modify(**kwargs)
        else:
            cu = None

        was_replaced = cu is not None
        return was_replaced

    def get_card(self):
        """Gets the customer's default card

        See:
        - https://stripe.com/docs/api/cards/list
        - https://stripe.com/docs/api/customers/object
        """
        stripe_customer = self.retrieve()
        card_id = stripe_customer['default_source']
        if card_id:
            card = self.retrieve_card(card_id)
        else:
            card = None

        return card

    def get_cards(self):
        args = (
            self.stripe_id,
        )
        kwargs = {
            'object': 'card',
        }

        response = safe_stripe_call(
            self.STRIPE_API_CLASS.list_sources,
            *args,
            **kwargs
        )
        cards = response['data'] if response else []

        return cards

    def has_card(self):
        """Determines whether this StripeCustomer has a card
        """
        cards = self.get_cards()
        has_card = len(cards) > 0
        return has_card

    ##
    # subscriptions

    @property
    def subscription_obj(self):
        return self.make_subscription_obj()

    def make_subscription_obj(self, subscription_id=None):
        """Creates a subscription object to make it easier to handle this
        """
        return BaseStripeSubscription(
            stripe_id=subscription_id,
            live_mode=self.live_mode,
            customer=self
        )

    def create_subscription(self, price_or_plan, invoice=True):
        """Creates a new Subscription for this Customer

        https://stripe.com/docs/api/subscriptions/create
        """
        stripe_subscription = self.subscription_obj.create(price_or_plan, invoice=invoice)
        return stripe_subscription

    def retrieve_subscription(self, subscription_id):
        """Retrieves a Subscription for this Customer

        https://stripe.com/docs/api/subscriptions/retrieve
        """
        if subscription_id:
            subscription = self.make_subscription_obj(
                subscription_id
            ).retrieve()
        else:
            # missing subscription id
            subscription = None

        return subscription

    def change_subscription_plan(self, subscription_id, new_price_or_plan, prorate=True, invoice=True):
        """Changes the plan on a Subscription for this Customer

        NOTE: This function/model only assumes one current active price per subscription

        https://stripe.com/docs/api/subscriptions/retrieve
        https://stripe.com/docs/api/subscriptions/update
        https://stripe.com/docs/billing/migration/migrating-prices#subscriptions
        """
        stripe_subscription = self.retrieve_subscription(subscription_id)
        if stripe_subscription:
            item = {
                'id': stripe_subscription['items']['data'][0]['id'],
            }
            if type(new_price_or_plan) == str:
                item['price'] = new_price_or_plan
            elif type(new_price_or_plan) == dict:
                item['price_data'] = new_price_or_plan
            else:
                raise Exception('Unsupported price_or_plan type: %s' % type(new_price_or_plan))

            kwargs = {
                'items': [
                    # NOTE: currently only 1 subscription item is handled
                    item,
                ],
                # https://stripe.com/docs/billing/subscriptions/billing-cycle#prorations
                'proration_behavior': 'create_prorations' if prorate else 'none',
            }
            updated_subscription = self.make_subscription_obj(
                subscription_id
            ).modify(
                **kwargs
            )

            if updated_subscription and invoice:
                # Note on Prorations:
                # If the new plan is more expensive, a payment will happen right away
                # Create the invoice and trust that Stripe handles it correctly :)
                #
                # See: https://stripe.com/docs/billing/subscriptions/billing-cycle#prorations
                self.create_invoice_and_pay()
            else:
                # do nothing, not invoicing :)
                pass
        else:
            updated_subscription = None

        return updated_subscription

    def free_upgrade_or_downgrade(self, subscription_id, new_price_or_plan):
        """Updates the plan on a Subscription for this Customer

        Does an immediate upgrade or downgrade to the new plan, but does
        not charge the Customer.
        This can be used, for example, when providing a free upgrade as
        a courtesy, or for admin-initiated subscription plan changes.

        If intending to charge the customer immediately at time of change
        or with proration, use `change_subscription_plan(prorate=True, invoice=True)` instead.

        https://stripe.com/docs/billing/subscriptions/prorations#disable-prorations
        https://stripe.com/docs/api#update_subscription
        """
        updated_subscription = self.change_subscription_plan(
            subscription_id,
            new_price_or_plan,
            prorate=False,
            invoice=False
        )
        return updated_subscription

    def cancel_subscription(self, subscription_id):
        """Cancels a Subscription for this Customer

        https://stripe.com/docs/api/subscriptions/cancel

        Returns:
        - True if `subscription_id` was canceled
        - False if `subscription_id` was not found
        """
        was_deleted = self.make_subscription_obj(
            subscription_id
        ).cancel()
        return was_deleted

    ##
    # delete

    def delete(self):
        """Deletes a customer

        https://stripe.com/docs/api/python#delete_customer
        """
        stripe_customer = self.retrieve()
        if stripe_customer:
            obj = safe_stripe_call(
                stripe_customer.delete
            )
            if obj:
                super(BaseStripeCustomer, self).delete()
            else:
                pass
        else:
            pass


class BaseStripeSubscription(BaseStripeModel):
    """Django model for Stripe Subscription

    NOTE: This class is just used for structural purposes for now, and not intended to be persisted

    https://stripe.com/docs/api/subscriptions
    """
    # class attributes
    STRIPE_API_CLASS = stripe.Subscription

    # fields
    # overrides `stripe_id`: unlike others, this will get set after creating
    stripe_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    customer = models.ForeignKey(htk_setting('HTK_STRIPE_CUSTOMER_MODEL'), related_name='subscriptions')

    def create(self, price_or_plan, invoice=True):
        """Creates a new Subscription

        https://stripe.com/docs/api/subscriptions/create
        """
        _initialize_stripe(live_mode=self.live_mode)

        item = {}
        if type(price_or_plan) == str:
            item['price'] = price_or_plan
        elif type(price_or_plan) == dict:
            item['price_data'] = price_or_plan
        else:
            raise Exception('Unsupported price_or_plan type: %s' % type(price_or_plan))

        kwargs = {
            'customer': self.customer.stripe_id,
            'items': [
                item,
            ],
        }
        stripe_subscription = safe_stripe_call(
            self.STRIPE_API_CLASS.create,
            **kwargs
        )

        if stripe_subscription:
            self.stripe_id = stripe_subscription['id']
            if invoice:
                self.customer.create_invoice_and_pay()
            else:
                pass
        else:
            pass

        return stripe_subscription

    def modify(self, **kwargs):
        """Modifies a Subscription plan

        https://stripe.com/docs/api/subscriptions/update
        """
        args = (
            self.stripe_id,
        )
        subscription = safe_stripe_call(
            self.STRIPE_API_CLASS.modify,
            *args,
            **kwargs
        )
        return subscription

    def cancel(self):
        """Cancels a Subscription for this Customer

        https://stripe.com/docs/api/subscriptions/cancel

        Returns:
        - True if subscription was canceled
        - False if subscription was not found
        """
        subscription = self.retrieve()

        if subscription:
            _ = safe_stripe_call(
                self.STRIPE_API_CLASS.delete,
                *args
            )
            was_deleted = True
        else:
            was_deleted = False

        return was_deleted



class BaseStripeProduct(BaseStripeModel):
    """Django model for Stripe Product

    https://stripe.com/docs/api/products
    """
    # class attributes
    STRIPE_API_CLASS = stripe.Product

    # fields
    name = models.CharField(max_length=64)
    product_type = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    statement_descriptor = models.CharField(max_length=22)

    class Meta:
        abstract = True

    def create(self):
        """Tries to create a product

        Will fail if product with the same Stripe id already exists
        """
        _initialize_stripe(live_mode=self.live_mode)
        stripe_product = safe_stripe_call(
            self.STRIPE_API_CLASS.create,
            **{
                'id': self.stripe_id,
                'name': self.name,
                'type': StripeProductType(self.product_type).name,
                'active': self.active,
                'statement_descriptor': self.statement_descriptor,
            }
        )
        return stripe_product


class BaseStripePrice(BaseStripeModel):
    """Django model for Stripe Price

    See: https://stripe.com/docs/api/prices
    """
    # class attributes
    STRIPE_API_CLASS = stripe.Price

    # fields
    # overrides `stripe_id`: unlike others, this will get set after creating
    stripe_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    product = models.ForeignKey(htk_setting('HTK_STRIPE_PRODUCT_MODEL'), related_name='prices')
    unit_amount = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=3, default=DEFAULT_STRIPE_CURRENCY)
    active = models.BooleanField(default=True)
    nickname = models.CharField(max_length=64, blank=True)

    class Meta:
        abstract = True

        unique_together = (
            ('live_mode', 'product_id', 'unit_amount', 'currency'),
        )

    def create(self):
        """Tries to create a price

        Will fail if price with the same Stripe id already exists

        https://stripe.com/docs/api/prices/create
        """
        _initialize_stripe(live_mode=self.live_mode)

        if self.stripe_id is not None:
            stripe_price = self.retrieve()
        else:
            stripe_product = self.product.retrieve()
            if stripe_product is None:
                # create the Product if it hasn't been created yet
                self.product.create()
            else:
                # do nothing
                pass

            stripe_price = safe_stripe_call(
                self.STRIPE_API_CLASS.create,
                **{
                    'currency': self.currency,
                    'product': self.product.stripe_id,
                    'unit_amount': self.unit_amount,
                    'active': self.active,
                    'nickname': self.nickname,
                }
            )

            self.stripe_id = stripe_price['id']
            self.save()

        return stripe_price


class BaseStripePlan(BaseStripeModel):
    """Django model for Stripe Plan

    See: https://stripe.com/docs/api/plans

    New integrations should use `BaseStripePrice`
    """
    STRIPE_API_CLASS = stripe.Plan

    # fields
    product_id = models.CharField(max_length=255)
    # TODO
    # product = models.ForeignKey(htk_setting('HTK_STRIPE_PRODUCT_MODEL'), related_name='plans')
    amount = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=3, default=DEFAULT_STRIPE_CURRENCY)
    interval = models.PositiveIntegerField()
    interval_count = models.PositiveIntegerField(default=1)
    nickname = models.CharField(max_length=64, blank=True)
    trial_period_days = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True

        unique_together = (
            ('stripe_id', 'live_mode',),
        )

    def create(self):
        """Tries to create a plan

        Will fail if plan with the same Stripe id already exists
        """
        _initialize_stripe(live_mode=self.live_mode)
        stripe_plan = safe_stripe_call(
            self.STRIPE_API_CLASS.create,
            **{
                'id': self.stripe_id,
                'product': self.product_id,
                'amount': self.amount,
                'currency': self.currency,
                'interval': StripePlanInterval(self.interval).name,
                'interval_count': self.interval_count,
                'nickname': self.nickname,
                'trial_period_days': self.trial_period_days,
            }
        )
        return stripe_plan


class AbstractStripeCustomerHolder(models.Model):
    stripe_customer = models.OneToOneField(
        settings.HTK_STRIPE_CUSTOMER_MODEL,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT,
        related_name=htk_setting('HTK_STRIPE_CUSTOMER_HOLDER_RELATED_NAME')
    )

    class Meta:
        abstract = True

    def get_stripe_customer_email(self):
        raise Exception('Subclass must implement this abstract function')

    def get_stripe_customer_description(self):
        raise Exception('Subclass must implement this abstract function')

    def create_stripe_customer(self, card=None):
        """Creates a new StripeCustomer object for this User if one does not exist

        If `card` is passed in, will also create the card for the customer
        """
        if self.stripe_customer:
            pass
        else:
            from htk.lib.stripe_lib.utils import create_customer
            email = self.get_stripe_customer_email()
            description = self.get_stripe_customer_description()
            customer, stripe_customer = create_customer(card=card, email=email, description=description)
            self.stripe_customer = customer
            self.save()
        return self.stripe_customer

    def add_or_replace_credit_card(self, card):
        """Add or replace the credit card on file for this User

        Creates a new StripeCustomer object if one does not exist yet
        """
        was_added_or_replaced = False
        if self.stripe_customer:
            was_replaced = self.stripe_customer.replace_card(card)
            was_added_or_replaced = was_replaced
        else:
            customer = self.create_stripe_customer(card=card)
            was_added_or_replaced = customer is not None
        return was_added_or_replaced
