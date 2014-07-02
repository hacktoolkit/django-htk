import stripe

from htk.utils import htk_setting

def _initialize_stripe():
    stripe.api_key = htk_setting('HTK_STRIPE_API_SECRET_KEY')
    stripe.api_version = htk_setting('HTK_STRIPE_API_VERSION')

def charge_card(stripe_token, amount, description=''):
    """Charges a card, one time

    https://stripe.com/docs/tutorials/charges
    https://stripe.com/docs/api/python#charges
    """
    _initialize_stripe()
    try:
        charge = stripe.Charge.create(
            amount=amount, # amount in cents
            currency='usd',
            card=stripe_token,
            description=''
        )
    except stripe.CardError, e:
        # The card has been declined
        charge = None
    return charge

def create_customer(stripe_token, description=''):
    """Create a Customer

    https://stripe.com/docs/tutorials/charges#saving-credit-card-details-for-later
    https://stripe.com/docs/api/python#create_customer
    """
    _initialize_stripe()
    stripe_customer = stripe.Customer.create(
        card=stripe_token,
        description=description
    )
    customer = StripeCustomer.objects.create(
        stripe_id=stripe_customer.id
    )
    return customer

####################
# Import these last to prevent circular import
from htk.lib.stripe_lib.models import StripeCustomer
