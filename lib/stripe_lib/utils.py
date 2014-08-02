import rollbar
import stripe

from django.conf import settings

from htk.utils import htk_setting

def _initialize_stripe():
    stripe.api_key = get_stripe_secret_key()
    stripe.api_version = htk_setting('HTK_STRIPE_API_VERSION')
    return stripe

def get_stripe_public_key():
    if settings.TEST or htk_setting('HTK_STRIPE_LIVE_MODE', True):
        public_key = htk_setting('HTK_STRIPE_API_PUBLIC_KEY_TEST')
    else:
        public_key = htk_setting('HTK_STRIPE_API_PUBLIC_KEY_LIVE')
    return public_key

def get_stripe_secret_key():
    if settings.TEST or htk_setting('HTK_STRIPE_LIVE_MODE', True):
        secret_key = htk_setting('HTK_STRIPE_API_SECRET_KEY_TEST')
    else:
        secret_key = htk_setting('HTK_STRIPE_API_SECRET_KEY_LIVE')
    return secret_key

def get_stripe_customer_model():
    from htk.utils.general import resolve_model_dynamically
    StripeCustomerModel = resolve_model_dynamically(settings.HTK_STRIPE_CUSTOMER_MODEL)
    return StripeCustomerModel

def safe_stripe_call(func, *args, **kwargs):
    """Wrapper function for calling Stripe API

    Handles all the possible errors
    https://stripe.com/docs/api/python#errors
    """
    result = None
    try:
        result = func(*args, **kwargs)
    except stripe.error.CardError, e:
        # Since it's a decline, stripe.error.CardError will be caught
        body = e.json_body
        err  = body['error']

        print "Status is: %s" % e.http_status
        print "Type is: %s" % err['type']
        print "Code is: %s" % err['code']
        # param is '' in this case
        print "Param is: %s" % err['param']
        print "Message is: %s" % err['message']
        rollbar.report_exc_info()
    except stripe.error.InvalidRequestError, e:
        # Invalid parameters were supplied to Stripe's API
        rollbar.report_exc_info()
    except stripe.error.AuthenticationError, e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        rollbar.report_exc_info()
    except stripe.error.APIConnectionError, e:
        # Network communication with Stripe failed
        rollbar.report_exc_info()
    except stripe.error.StripeError, e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        rollbar.report_exc_info()
    except Exception, e:
        # Something else happened, completely unrelated to Stripe
        rollbar.report_exc_info()
    return result

def create_token(card_dict):
    _initialize_stripe()
    token = safe_stripe_call(
        stripe.Token.create,
        **{
            'card' : card_dict,
        }
    )
    return token

def charge_card(card, amount, description=''):
    """Charges a card, one time

    It is preferred to create a customer and charge the customer

    https://stripe.com/docs/api/python#create_charge
    https://stripe.com/docs/tutorials/charges
    https://stripe.com/docs/api/python#charges
    """
    _initialize_stripe()
    charge = safe_stripe_call(
        stripe.Charge.create,
        **{
            'amount' : amount, # amount in cents
            'currency' : 'usd',
            'card' : card,
            'description' : '',
        }
    )
    return charge

def create_customer(card, description=''):
    """Create a Customer

    https://stripe.com/docs/tutorials/charges#saving-credit-card-details-for-later
    https://stripe.com/docs/api/python#create_customer
    """
    _initialize_stripe()

    stripe_customer = safe_stripe_call(
        stripe.Customer.create,
        **{
            'card' : card,
            'description' : description,
        }
    )
    if stripe_customer:
        StripeCustomerModel = get_stripe_customer_model()
        if StripeCustomerModel:
            customer = StripeCustomerModel.objects.create(
                stripe_id=stripe_customer.id
            )
        else:
            customer = None
    else:
        customer = None
    return customer, stripe_customer

####################
# Import these last to prevent circular import
