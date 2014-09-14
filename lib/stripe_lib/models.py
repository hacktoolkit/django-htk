import stripe

from django.db import models

from htk.lib.stripe_lib.enums import StripePlanInterval
from htk.lib.stripe_lib.utils import _initialize_stripe
from htk.lib.stripe_lib.utils import safe_stripe_call
from htk.lib.stripe_lib.constants.general import *

class BaseStripeCustomer(models.Model):
    stripe_id = models.CharField(max_length=255)
    live_mode = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __unicode__(self):
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
    # payments

    def charge(self, amount=0, currency=DEFAULT_STRIPE_CURRENCY):
        """Charges a Customer
        """
        _initialize_stripe(live_mode=self.live_mode)
        ch = safe_stripe_call(
            stripe.Charge.create,
            **{
                'amount' : amount,
                'currency' : currency,
                'customer' : self.stripe_id,
            }
        )
        return ch

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
                stripe_customer.cards.create,
                **{
                    'card' : card,
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
            stripe_customer.card = card
            cu = safe_stripe_call(
                stripe_customer.save,
                **{}
            )
        else:
            cu = None
        was_replaced = cu is not None
        return was_replaced

    def get_card(self):
        stripe_customer = self.retrieve()
        cards = safe_stripe_call(
            stripe_customer.cards.all,
            **{
                'limit' : 1,
            }
         )
        cards = cards.get('data')
        if len(cards) > 0:
            card = cards[0]
        else:
            card = None
        return card

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
        stripe_customer = self.retrieve()
        subscription = safe_stripe_call(
            stripe_customer.subscriptions.retrieve,
            **{
                'id' : subscription_id,
            }
        )
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

    def cancel_subscription(self, subscription_id):
        """Cancels a Subscription for this Customer

        https://stripe.com/docs/api#cancel_subscription
        """
        subscription = self.retrieve_subscription(subscription_id)
        subscription.delete()
        was_deleted = True
        return was_deleted

    ##
    # delete

    def delete(self):
        """Deletes a customer

        https://stripe.com/docs/api/python#delete_customer
        """
        stripe_customer = self.retrieve()
        obj = safe_stripe_call(
            stripe_customer.delete
        )
        if obj:
            super(BaseStripeCustomer, self).delete()
        else:
            pass

class BaseStripePlan(models.Model):
    stripe_id = models.CharField(max_length=255)
    live_mode = models.BooleanField(default=False)
    amount = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=3, default=DEFAULT_STRIPE_CURRENCY)
    interval = models.PositiveIntegerField()
    interval_count = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=64)
    trial_period_days = models.PositiveIntegerField(default=0)
    statement_description = models.CharField(max_length=15)

    class Meta:
        abstract = True

    def __unicode__(self):
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
                'amount' : self.amount,
                'currency' : self.currency,
                'interval' : StripePlanInterval(self.interval).name,
                'interval_count' : self.interval_count,
                'name' : self.name,
                'trial_period_days' : self.trial_period_days,
                'statement_description' : self.statement_description,
            }
        )
        return stripe_plan
