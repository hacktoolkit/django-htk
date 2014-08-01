import datetime
import random

from django.test import TestCase

from htk.lib.stripe_lib.constants import *
from htk.lib.stripe_lib.utils import _initialize_stripe
from htk.lib.stripe_lib.utils import charge_card
from htk.lib.stripe_lib.utils import create_customer
from htk.lib.stripe_lib.utils import safe_stripe_call

class StripeLibTestCase(TestCase):
    def _get_test_card_number(self, card_type):
        cards = STRIPE_TEST_CARDS[card_type]
        card = random.choice(cards)
        card_number = card['number']
        return card_number

    def _create_recipient(self):
        stripe = _initialize_stripe()
        recipient = safe_stripe_call(
            stripe.Recipient.create,
            **{
                'name' : 'John Doe',
                'type' : 'individual',
            }
        )
        self.assertEqual(STRIPE_ID_PREFIX_RECIPIENT, recipient.id[:len(STRIPE_ID_PREFIX_RECIPIENT)])
        return recipient

    def _get_card_dict(self, card_type='visa'):
        """Gets a random card dictionary
        """
        card_number = self._get_test_card_number(card_type)
        card_dict = {
            'number' : card_number,
            'exp_month' : '12',
            'exp_year' : '%s' % (datetime.date.today().year + 1),
            'cvc' : '123',
            'name' : 'Jane Doe',
        }
        return card_dict

    def _create_customer_with_card(self):
        card_dict = self._get_card_dict()
        customer, stripe_customer = create_customer(card_dict, description='Test creating a customer with card')
        self.assertEqual(STRIPE_ID_PREFIX_CUSTOMER, stripe_customer.id[:len(STRIPE_ID_PREFIX_CUSTOMER)])
        return customer

    def test_create_recipient_with_card(self):
        recipient = self._create_recipient()
        card_dict = self._get_card_dict(card_type='visa_debit')
        card = safe_stripe_call(
            recipient.cards.create,
            **{
                'card' : card_dict,
            }
        )
        self.assertEqual(STRIPE_ID_PREFIX_CARD, card.id[:len(STRIPE_ID_PREFIX_CARD)])

    def test_create_customer_with_card(self):
        customer = self._create_customer_with_card()

    def test_charge_card(self):
        """Actually, charge a customer
        """
        card_dict = self._get_card_dict()
        charge = charge_card(card_dict, 31415, description='Test charge for PI-inspired $314.15')
        self.assertEqual(STRIPE_ID_PREFIX_CHARGE, charge.id[:len(STRIPE_ID_PREFIX_CHARGE)])
