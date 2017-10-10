from django.shortcuts import redirect

from social_core.pipeline.partial import partial

from htk.apps.accounts.emails import welcome_email
from htk.apps.accounts.session_keys import *
from htk.apps.accounts.utils import associate_user_email
from htk.apps.accounts.utils import get_incomplete_signup_user_by_email
from htk.apps.accounts.utils import get_user_by_email
from htk.apps.accounts.view_helpers import redirect_to_social_auth_complete
from htk.utils import htk_setting

# Custom Pipeline Functions
# https://django-social-auth.readthedocs.org/en/v0.7.22/pipeline.html
#
# available in kwargs
#
# backend - current social authentication backend (`backend.name`)
# uid - given by authentication provider
# details - user details given by authentication provider
# user - already logged in user or newly created user
# is_new - if `user` is newly created

# 1. If there is no email, have the user enter an email
# 2. Check association. If there is an account with that email:
#    a. "An account with this email address already exists. Please log in to link your {{ SOCIAL }} account."
#    b. "An account with this email address is already linked to {{ SOCIAL }}. Please create a new account using a different email address."
# 3. Create the account with the username and email

def python_social_auth_shim(pipeline_func):
    """Shim layer decorator for django-social-auth to python-social auth migration
    pipeline complete wasn't passing the request object, but the strategy object instead
    """
    def wrapped(strategy, *args, **kwargs):
        if not kwargs.get('request'):
            request = strategy.request
            kwargs['request'] = request
        return pipeline_func(*args, **kwargs)
    return wrapped

def reset_session_keys(strategy, *args, **kwargs):
    """Reset a bunch of keys used as part of the social auth flow
    This is to prevent partially-completed values from a previous flow from affecting a new social auth flow
    """
    for key in SOCIAL_AUTH_FLOW_KEYS:
        if strategy.request.session.get(key):
            del strategy.request.session[key]
    return None

@partial
def check_email(strategy, details, user=None, *args, **kwargs):
    """Ask the user to enter the email if we don't have one yet

    The pipeline process was cut prior to this custom pipeline function, and will resume to this same function after completing
    """
    response = None
    if user is None:
        strategy.request.session['backend'] = kwargs.get('current_partial').backend
        social_email = details.get('email')
        collected_email = strategy.request.session.get(SOCIAL_REGISTRATION_SETTING_EMAIL)
        if social_email:
            # email available from social auth
            user = get_user_by_email(social_email)
            if user and user.is_active:
                # a user is already associated with this email
                # TODO: there is an error with linking accounts...
                strategy.request.session[SOCIAL_REGISTRATION_SETTING_EMAIL] = social_email
                if user.has_usable_password():
                    # user should log into the existing account with a password
                    url_name = htk_setting('HTK_ACCOUNTS_REGISTER_SOCIAL_LOGIN_URL_NAME')
                else:
                    # no password was set, so user must log in with another social auth account
                    url_name = htk_setting('HTK_ACCOUNTS_REGISTER_SOCIAL_ALREADY_LINKED_URL_NAME')
                response = redirect(url_name)
        elif collected_email:
            # email provided by user
            details['email'] = collected_email
            response = { 'details' : details }
        else:
            # no email provided from social auth
            strategy.request.session[SOCIAL_REGISTRATION_SETTING_MISSING_EMAIL] = True
            url_name = htk_setting('HTK_ACCOUNTS_REGISTER_SOCIAL_EMAIL_URL_NAME')
            response = redirect(url_name)

    return response

@partial
def check_terms_agreement(strategy, details, user=None, *args, **kwargs):
    """
    Ask the user to agree to Privacy Policy and Terms of Service
    """
    response = None
    if user is None:
        agreed_to_terms = strategy.request.session.get(SOCIAL_REGISTRATION_SETTING_AGREED_TO_TERMS, False)
        if not agreed_to_terms:
            email = details.get('email')
            strategy.request.session[SOCIAL_REGISTRATION_SETTING_EMAIL] = email
            url_name = htk_setting('HTK_ACCOUNTS_REGISTER_SOCIAL_EMAIL_AND_TERMS_URL_NAME')
            response = redirect(url_name)
        else:
            pass
    else:
        pass
    return response

def check_incomplete_signup(strategy, details, user=None, *args, **kwargs):
    """Checks for an incomplete signup, and sets that User instead
    """
    response = None
    if user is None:
        social_email = details.get('email')
        user = get_incomplete_signup_user_by_email(social_email)
        response = {
            'user' : user,
            'is_new' : user is None,
        }
    return response

def set_username(strategy, details, user, social, *args, **kwargs):
    """This pipeline function can be used to set UserProfile.has_username_set = True

    Normally not used if the auto-generated username is ugly
    """
    if not user:
        return None

    response = None
    if hasattr(user, 'profile'):
        user_profile = user.profile
        if hasattr(user_profile, 'has_username_set'):
            user_profile.has_username_set = True
            user_profile.save()
    return response

def associate_email(strategy, details, user, social, *args, **kwargs):
    """Associate email with the user
    """
    if not user or not social:
        return None

    response = None

    email = details.get('email')
    domain = strategy.request.get_host()
    # Should confirm if the email was provided by the social auth provider, not the user
    # i.e. SOCIAL_REGISTRATION_SETTING_MISSING_EMAIL was False
    confirmed = not(strategy.request.session.get(SOCIAL_REGISTRATION_SETTING_MISSING_EMAIL, False))
    user_email = associate_user_email(user, email, domain, confirmed=confirmed)

    if user_email:
        # need to update the User with the activated one, so that it doesn't get overwritten later on
        response = {
            'user': user_email.user,
        }
    return response

def handle_new_user(user, is_new, *args, **kwargs):
    """Do stuff if the account was newly created
    """
    if not user:
        return None

    if is_new:
        # send a welcome email to the user, regardless of email confirmation status
        welcome_email(user)

def post_connect(user, social, *args, **kwargs):
    response = None
    return response
