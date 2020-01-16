# HTK Imports
from htk.api.utils import extract_post_params
from htk.lib.stripe_lib.forms import CreditCardForm


def get_stripe_card_dict_from_post_data(post_data):
    """Gets a Stripe card dict from `post_data` if possible
    """
    stripe_card_dict = None
    credit_card_params = extract_credit_card_params(post_data)
    if credit_card_params is not None:
        credit_card_form = CreditCardForm(credit_card_params)
        if credit_card_form.is_valid():
            # need to call is_valid so that form.cleaned_data is populated
            # defer real validation to Stripe
            stripe_card_dict = credit_card_form.get_stripe_card_dict()
    return stripe_card_dict

def extract_credit_card_params(post_data):
    """Extract credit card form params from `post_data`
    """
    blank_credit_card_form = CreditCardForm()
    expected_params = list(blank_credit_card_form.fields.keys())
    try:
        credit_card_params = extract_post_params(post_data, expected_params)
    except:
        credit_card_params = None
    return credit_card_params
