import rollbar
import stripe

from django.conf import settings

from htk.utils import htk_setting
from htk.utils.general import resolve_model_dynamically

##
# general helpers

def _initialize_stripe(live_mode=False):
    stripe.api_key = get_stripe_secret_key(live_mode=live_mode)
    stripe.api_version = htk_setting('HTK_STRIPE_API_VERSION')
    return stripe

def get_stripe_public_key(live_mode=False):
    if not live_mode or settings.TEST or not htk_setting('HTK_STRIPE_LIVE_MODE'):
        public_key = htk_setting('HTK_STRIPE_API_PUBLIC_KEY_TEST')
    else:
        public_key = htk_setting('HTK_STRIPE_API_PUBLIC_KEY_LIVE')
    return public_key

def get_stripe_secret_key(live_mode=False):
    if not live_mode or settings.TEST or not htk_setting('HTK_STRIPE_LIVE_MODE'):
        secret_key = htk_setting('HTK_STRIPE_API_SECRET_KEY_TEST')
    else:
        secret_key = htk_setting('HTK_STRIPE_API_SECRET_KEY_LIVE')
    return secret_key

def get_stripe_customer_model():
    from htk.utils.general import resolve_model_dynamically
    if hasattr(settings, 'HTK_STRIPE_CUSTOMER_MODEL'):
        StripeCustomerModel = resolve_model_dynamically(settings.HTK_STRIPE_CUSTOMER_MODEL)
    else:
        StripeCustomerModel = None
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

##
# Stripe API

def create_token(card_dict, live_mode=False):
    _initialize_stripe(live_mode=live_mode)
    token = safe_stripe_call(
        stripe.Token.create,
        **{
            'card' : card_dict,
        }
    )
    return token

def charge_card(card, amount, description='', live_mode=False):
    """Charges a card, one time

    It is preferred to create a customer and charge the customer

    https://stripe.com/docs/api/python#create_charge
    https://stripe.com/docs/tutorials/charges
    https://stripe.com/docs/api/python#charges
    """
    _initialize_stripe(live_mode=live_mode)
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

def create_customer(card, description='', live_mode=False):
    """Create a Customer

    https://stripe.com/docs/tutorials/charges#saving-credit-card-details-for-later
    https://stripe.com/docs/api/python#create_customer
    """
    _initialize_stripe(live_mode=live_mode)

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

##
# events and webhooks

def retrieve_event(event_id, live_mode=False):
    """Retrieve the Stripe event

    Only works when `live_mode=True`
    """
    _initialize_stripe(live_mode=live_mode)
    event = safe_stripe_call(
        stripe.Event.retrieve,
        *(
            event_id,
        )
    )
    return event

def get_event_type(event):
    """Gets the event type

    `event` can either be a StripeEvent object or just a JSON dictionary
    """
    if type(event) == dict:
        event_type = event.get('type', None)
    else:
        event_type = event.type
    return event_type

def get_event_handler(event):
    """Gets the event handler for a Stripe webhook event, if available
    """
    event_handlers = htk_setting('HTK_STRIPE_EVENT_HANDLERS', {})
    event_type = get_event_type(event)
    event_handler_module_str = event_handlers.get(event_type)
    if event_handler_module_str:
        event_handler = resolve_method_dynamically(event_handler_module_str)
    else:
        event_handler = None
    return event_handler

def handle_event(event, request=None):
    """Handles a Stripe webhook event

    https://stripe.com/docs/api#event_types
    """
    event_handler = get_event_handler(event)
    if event_handler:
        event_handler(event)
    elif htk_setting('HTK_STRIPE_LOG_UNHANDLED_EVENTS_ROLLBAR'):
        rollbar.report_message('Stripe Event: %s' % get_event_type(event), 'info', request)
    else:
        pass
