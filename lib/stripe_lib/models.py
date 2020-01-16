# Python Standard Library Imports

# Third Party / PIP Imports
import rollbar
import stripe

# Django Imports
from django.conf import settings
from django.db import models

# HTK Imports
from htk.lib.stripe_lib.constants.general import *
from htk.lib.stripe_lib.enums import StripePlanInterval
from htk.lib.stripe_lib.enums import StripeProductType
from htk.lib.stripe_lib.utils import _initialize_stripe
from htk.lib.stripe_lib.utils import safe_stripe_call
from htk.utils import htk_setting
from htk.utils.request import get_current_request


class BaseStripeCustomer(models.Model):
    stripe_id = models.CharField(max_length=255)
    live_mode = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        value = '%s - %s' % (self.__class__.__name__, self.stripe_id,)
        return value

    def retrieve(self):
        """Retrieves an existing customer

        https://stripe.com/docs/api/python#retrieve_customer
        """
        _initialize_stripe(live_mode=self.live_mode)
        stripe_customer = safe_stripe_call(
            stripe.Customer.retrieve,
            *(
                self.stripe_id,
            )
        )
        return stripe_customer

    ##
    # customer details

    def update_email(self, email=None):
        """Updates the email for this Customer
        """
        stripe_customer = None
        if email is not None:
            stripe_customer = self.retrieve()
            if stripe_customer.email != email:
                # TODO: it might make sense to implement some kind of update-if-changed, or perhaps the Stripe library is already smart about it?
                stripe_customer.email = email
                stripe_customer = safe_stripe_call(
                    stripe_customer.save,
                    **{}
                )
            else:
                pass
        else:
            pass
        return stripe_customer

    ##
    # payments

    def charge(self, amount=0, currency=DEFAULT_STRIPE_CURRENCY, metadata=None):
        """Charges a Customer
        """
        if metadata is None:
            metadata = {}
        _initialize_stripe(live_mode=self.live_mode)
        ch = safe_stripe_call(
            stripe.Charge.create,
            **{
                'amount' : amount,
                'currency' : currency,
                'customer' : self.stripe_id,
                'metadata' : metadata
            }
        )
        return ch

    def get_charges(self):
        _initialize_stripe(live_mode=self.live_mode)
        charges = safe_stripe_call(
            stripe.Charge.all,
            **{
                'customer' : self.stripe_id,
            }
        )
        charges = charges.get('data')
        return charges

    def create_invoice(self):
        """Create an Invoice for this Customer to pay any outstanding invoice items such as when upgrading plans

        https://stripe.com/docs/api#create_invoice
        """
        _initialize_stripe(live_mode=self.live_mode)
        invoice = safe_stripe_call(
            stripe.Invoice.create,
            **{
                'customer' : self.stripe_id,
            }
        )
        return invoice

    def create_invoice_and_pay(self):
        """
        After creating the Invoice, have the Customer immediately pay it

        https://stripe.com/docs/api#pay_invoice
        """
        invoice = self.create_invoice()
        if invoice:
            invoice.pay()
        else:
            rollbar.report_message('Could not create invoice for Customer %s' % self.stripe_id, 'error')

    ##
    # cards

    def add_card(self, card):
        """Add an additional credit card to the customer

        https://stripe.com/docs/api/python#create_card
        """
        stripe_customer = self.retrieve()
        if stripe_customer:
            stripe_card = safe_stripe_call(
                stripe_customer.sources.create,
                **{
                    'source' : card,
                }
            )
        else:
            stripe_card = None
        was_added = stripe_card is not None
        return was_added

    def replace_card(self, card):
        """Adds a new credit card and delete this Customer's old one

        WARNING: This deletes the old card. Use `add_card` instead to just add a card without deleting

        https://stripe.com/docs/api/python#update_customer
        """
        stripe_customer = self.retrieve()
        if stripe_customer:
            stripe_customer.source = card
            cu = safe_stripe_call(
                stripe_customer.save,
                **{}
            )
        else:
            cu = None
        was_replaced = cu is not None
        return was_replaced

    def get_card(self):
        """
        https://stripe.com/docs/api/python#list_cards
        """
        stripe_customer = self.retrieve()
        if stripe_customer:
            cards = safe_stripe_call(
                stripe_customer.sources.all,
                **{
                    'limit' : 1,
                    'object' : 'card',
                }
            )
            cards = cards.get('data')
            if len(cards) > 0:
                card = cards[0]
            else:
                card = None
        else:
            card = None
        return card

    def get_cards(self):
        stripe_customer = self.retrieve()
        if stripe_customer:
            cards = safe_stripe_call(
                stripe_customer.sources.all,
                **{
                    'object' : 'card',
                }
            )
            cards = cards.get('data')
        else:
            cards = []
        return cards

    def has_card(self):
        """Determines whether this StripeCustomer has a card
        """
        stripe_customer = self.retrieve()
        if stripe_customer:
            cards = safe_stripe_call(
                stripe_customer.sources.all,
                **{
                    'limit' : 1,
                    'object' : 'card',
                }
            )
            value = len(cards) > 0
        else:
            value = False
        return value

    ##
    # subscriptions

    def create_subscription(self, plan):
        """Creates a new Subscription for this Customer

        https://stripe.com/docs/api#create_subscription
        """
        stripe_customer = self.retrieve()
        subscription = safe_stripe_call(
            stripe_customer.subscriptions.create,
            **{
                'plan' : plan,
            }
        )
        return subscription

    def retrieve_subscription(self, subscription_id):
        """Retrieves a Subscription for this Customer

        https://stripe.com/docs/api#retrieve_subscription
        """
        subscription = None

        if subscription_id:
            stripe_customer = self.retrieve()
            if stripe_customer:
                subscription = safe_stripe_call(
                    stripe_customer.subscriptions.retrieve,
                    **{
                        'id' : subscription_id,
                    }
                )
            else:
                # missing Stripe customer
                pass
        else:
            # missing subscription id
            pass

        return subscription

    def change_subscription_plan(self, subscription_id, new_plan):
        """Changes the plan on a Subscription for this Customer

        https://stripe.com/docs/api#update_subscription
        """
        subscription = self.retrieve_subscription(subscription_id)
        if subscription:
            subscription.plan = new_plan
            #subscription.prorate = True
            subscription.save()

            # if the new plan is more expensive, pay right away
            # pro-ration is the default behavior
            # or, just naively create the invoice every time and trust that Stripe handles it correctly
            self.create_invoice_and_pay()
        else:
            pass
        return subscription

    def free_upgrade_or_downgrade(self, subscription_id, new_plan):
        """Updates the plan on a Subscription for this Customer

        Does an immediate upgrade or downgrade to the new plan, but does
        not charge the Customer.
        This can be used, for example, when providing a free upgrade as
        a courtesy, or for admin-initiated subscription plan changes.

        If intending to charge the customer immediately at time of change
        or with proration, use `change_subscription_plan()` instead.

        https://stripe.com/docs/billing/subscriptions/prorations#disable-prorations
        https://stripe.com/docs/api#update_subscription
        """
        subscription = self.retrieve_subscription(subscription_id)
        if subscription:
            subscription.plan = new_plan
            subscription.prorate = False
            subscription.save()
            # DO NOT CREATE AN INVOICE
        else:
            pass
        return subscription

    def cancel_subscription(self, subscription_id):
        """Cancels a Subscription for this Customer

        https://stripe.com/docs/api#cancel_subscription

        Returns:
        - True if `subscription_id` was canceled
        - False if `subscription_id` was not found
        """
        subscription = self.retrieve_subscription(subscription_id)
        if subscription:
            subscription.delete()
            was_deleted = True
        else:
            was_deleted = False
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


class BaseStripeProduct(models.Model):
    stripe_id = models.CharField(max_length=255)
    live_mode = models.BooleanField(default=False)
    name = models.CharField(max_length=64)
    product_type = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    statement_descriptor = models.CharField(max_length=22)

    class Meta:
        abstract = True

    def __str__(self):
        value = '%s - %s' % (self.__class__.__name__, self.stripe_id,)
        return value

    def create(self):
        """Tries to create a product

        Will fail if product with the same Stripe id already exists
        """
        _initialize_stripe(live_mode=self.live_mode)
        stripe_product = safe_stripe_call(
            stripe.Product.create,
            **{
                'id' : self.stripe_id,
                'name' : self.name,
                'type' : StripeProductType(self.product_type).name,
                'active' : self.active,
                'statement_descriptor' : self.statement_descriptor,
            }
        )
        return stripe_product


class BaseStripePlan(models.Model):
    stripe_id = models.CharField(max_length=255)
    live_mode = models.BooleanField(default=False)
    product_id = models.CharField(max_length=255)
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

    def __str__(self):
        value = '%s - %s' % (self.__class__.__name__, self.stripe_id,)
        return value

    def retrieve(self):
        """Retrieves an existing Plan
        """
        _initialize_stripe(live_mode=self.live_mode)
        stripe_plan = safe_stripe_call(
            stripe.Plan.retrieve,
            *(
                self.stripe_id,
            )
        )
        return stripe_plan

    def create(self):
        """Tries to create a plan

        Will fail if plan with the same Stripe id already exists
        """
        _initialize_stripe(live_mode=self.live_mode)
        stripe_plan = safe_stripe_call(
            stripe.Plan.create,
            **{
                'id' : self.stripe_id,
                'product' : self.product_id,
                'amount' : self.amount,
                'currency' : self.currency,
                'interval' : StripePlanInterval(self.interval).name,
                'interval_count' : self.interval_count,
                'nickname' : self.nickname,
                'trial_period_days' : self.trial_period_days,
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
