# Python Standard Library Imports

# Third Party / PIP Imports
import rollbar
import stripe

# Django Imports
from django.conf import settings

# HTK Imports
from htk.utils import htk_setting
from htk.utils.request import get_current_request

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
    if hasattr(settings, 'HTK_STRIPE_CUSTOMER_MODEL'):
        from htk.utils.general import resolve_model_dynamically
        StripeCustomerModel = resolve_model_dynamically(settings.HTK_STRIPE_CUSTOMER_MODEL)
    else:
        StripeCustomerModel = None
    return StripeCustomerModel


def get_stripe_customer_model_instance(customer_id, live_mode=False):
    """Gets the StripeCustomerModel object for `customer_id` if available
    """
    StripeCustomerModel = get_stripe_customer_model()
    try:
        customer = StripeCustomerModel.objects.get(
            stripe_id=customer_id,
            live_mode=live_mode
        )
    except StripeCustomerModel.DoesNotExist:
        customer = None
    return customer


def safe_stripe_call(func, *args, **kwargs):
    """Wrapper function for calling Stripe API

    Handles all the possible errors
    https://stripe.com/docs/api/python#errors
    """
    result = None

    def _log_error():
        request = get_current_request()
        extra_data = {
        }
        rollbar.report_exc_info(request=request, extra_data=extra_data)

    try:
        result = func(*args, **kwargs)
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        #body = e.json_body
        #err  = body['error']

        #print('Status is: {}'.format(e.http_status))
        #print('Type is: {}'.format(err.get('type')))
        #print('Code is: {}'.format(err.get('code')))
        ## param is '' in this case
        #print('Param is: {}'.format(err.get('param')))
        #print('Message is: {}'.format(err.get('message')))
        _log_error()
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        _log_error()
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        _log_error()
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        _log_error()
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        _log_error()
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        _log_error()

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


def create_customer(card=None, email=None, description=''):
    """Create a Customer

    https://stripe.com/docs/tutorials/charges#saving-credit-card-details-for-later
    https://stripe.com/docs/api/python#create_customer
    """
    live_mode = (settings.ENV_STAGE or settings.ENV_PROD) and htk_setting('HTK_STRIPE_LIVE_MODE')
    _initialize_stripe(live_mode=live_mode)

    params = {
        'email' : email,
        'description' : description,
    }
    if card:
        params['card'] = card
    else:
        pass

    stripe_customer = safe_stripe_call(
        stripe.Customer.create,
        **params
    )
    if stripe_customer:
        StripeCustomerModel = get_stripe_customer_model()
        if StripeCustomerModel:
            customer = StripeCustomerModel.objects.create(
                stripe_id=stripe_customer.id,
                live_mode=live_mode
            )
        else:
            customer = None
    else:
        customer = None
    return customer, stripe_customer


##
# events and webhooks


def retrieve_event(event_id, live_mode=False):
    """Retrieve the Stripe event by `event_id`

    Succeeds when `live_mode==True` and there a corresponding `event_id`
    Fails when event was generated from the Stripe dashboard webhook test

    https://stripe.com/docs/api#retrieve_event
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
        from htk.utils.general import resolve_method_dynamically
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
        event_handler(event, request=request)
    elif htk_setting('HTK_STRIPE_LOG_UNHANDLED_EVENTS'):
        # missing Stripe webhook event handler
        log_event(event, request=request)
    else:
        pass


def log_event(event, request=None, log_level='info', message=None):
    """Log the Stripe event `event`
    """
    live_mode = event.get('livemode', False)
    should_log = live_mode or htk_setting('HTK_STRIPE_LOG_TEST_MODE_EVENTS')
    if should_log:
        logger_type = htk_setting('HTK_STRIPE_EVENT_LOGGER')
        if logger_type == 'rollbar':
            _log_event_rollbar(event, request=None, log_level='info', message=None)
        else:
            # unrecognized Stripe event logger
            pass
    else:
        # do nothing
        pass


def _log_event_rollbar(event, request=None, log_level='info', message=None):
    """Log the Stripe event `event` to Rollbar
    """
    if message:
        message = '%s - Stripe Event: %s' % (message, get_event_type(event),)
    else:
        message = 'Stripe Event: %s' % get_event_type(event)
    extra_data = {
        'event' : event,
    }
    rollbar.report_message(message, log_level, request, extra_data=extra_data)
