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

    def add_card(self, card):
        """Add an additional credit card to the customer

        https://stripe.com/docs/api/python#create_card
        """
        stripe_customer = self.retrieve()
        if stripe_customer:
            safe_stripe_call(
                stripe_customer.cards.create,
                **{
                    'card' : card,
                }
            )
        else:
            pass

    def update_card(self, card):
        """Updates the customer's credit card and deletes the old one

        WARNING: This deletes the old card. Use `add_card` instead to just add a card without deleting

        https://stripe.com/docs/api/python#update_customer
        """
        stripe_customer = self.retrieve()
        stripe_customer.card = card
        stripe_customer.save()

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

        Will if plan with the same Stripe id already exists
        """
        _initialize_stripe(live_mode=self.live_mode)
        stripe_plan = safe_stripe_call(
            stripe.Plan.create,
            **{
                'id' : self.stripe_id,
                'amount' : self.amount,
                'interval' : StripePlanInterval(self.interval).name,
                'interval_count' : self.interval_count,
                'name' : self.name,
                'trial_period_days' : self.trial_period_days,
                'statement_description' : self.statement_description,
            }
        )
        return stripe_plan
