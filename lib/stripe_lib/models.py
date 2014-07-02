import stripe

from django.db import models

from htk.lib.stripe_lib.utils import _initialize_stripe

class StripeCustomer(models.Model):
    stripe_id = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def charge(self, amount=0, currency='usd'):
        """Charges a Customer
        """
        _initialize_stripe()
        ch = stripe.Charge.create(
            amount=amount,
            currency=currency,
            customer=self.stripe_id
        )
        return ch

    def retrieve(self):
        """Retrieves an existing customer

        https://stripe.com/docs/api/python#retrieve_customer
        """
        _initialize_stripe()
        cu = stripe.Customer.retrieve(stripe_id)
        return cu

    def add_card(self, card):
        """Add an additional credit card to the customer

        https://stripe.com/docs/api/python#create_card
        """
        cu = self.retrieve()
        cu.cards.create(card=card)

    def update_card(self, card):
        """Updates the customer's credit card and deletes the old one

        WARNING: This deletes the old card. Use `add_card` instead to just add a card without deleting

        https://stripe.com/docs/api/python#update_customer
        """
        cu = self.retrieve()
        cu.card = card
        cu.save()

    def delete(self):
        """Deletes a customer

        https://stripe.com/docs/api/python#delete_customer
        """
        cu = self.retrieve()
        cu.delete()
        super(StripeCustomer, self).delete()
