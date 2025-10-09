# Third Party (PyPI) Imports
from social_core.pipeline.partial import partial
from social_core.pipeline.social_auth import associate_user

# Django Imports
from django.shortcuts import redirect

# HTK Imports
from htk.apps.accounts.emails import welcome_email
from htk.apps.accounts.session_keys import (
    SOCIAL_AUTH_FLOW_KEYS,
    SOCIAL_REGISTRATION_SETTING_AGREED_TO_TERMS,
    SOCIAL_REGISTRATION_SETTING_EMAIL,
    SOCIAL_REGISTRATION_SETTING_MISSING_EMAIL,
)
from htk.apps.accounts.utils import (
    associate_user_email,
    get_incomplete_signup_user_by_email,
    get_user_by_email,
)
from htk.utils import htk_setting
from htk.utils.notifications import notify


# isort: off


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
#    a. "An account with this email address already exists. Please log in to link your
#        {{ SOCIAL }} account."
#    b. "An account with this email address is already linked to {{ SOCIAL }}. Please
#        create a new account using a different email address."
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

    This is to prevent partially-completed values from a previous flow from affecting a
    new social auth flow
    """
    for key in SOCIAL_AUTH_FLOW_KEYS:
        if strategy.request.session.get(key):
            del strategy.request.session[key]
    return None


@partial
def check_email(strategy, details, backend, uid, user=None, *args, **kwargs):
    """Ask the user to enter the email if we don't have one yet

    The pipeline process was cut prior to this custom pipeline function, and will
    resume to this same function after completing the social auth flow.
    """
    response = None
    if user is None:
        strategy.request.session['backend'] = kwargs.get(
            'current_partial'
        ).backend
        social_email = details.get('email')
        collected_email = strategy.request.session.get(
            SOCIAL_REGISTRATION_SETTING_EMAIL
        )
        if social_email:
            # Email provided by social auth provider (e.g., Google, Apple)
            # Look up existing user by email
            # NOTE: get_user_by_email() returns a User if:
            #   1. A confirmed UserEmail exists (UserEmail.is_confirmed=True), OR
            #   2. User.email matches and User.is_active=True, OR
            #   3. An incomplete signup exists (is_active=False, is_confirmed=False)
            user = get_user_by_email(social_email)
            if user:
                # Found an existing User (active, inactive, or incomplete signup)
                # with this email address
                auto_associate_backends = htk_setting(
                    'HTK_ACCOUNTS_SOCIAL_AUTO_ASSOCIATE_BACKENDS', []
                )
                backend_name = backend.name
                if backend_name in auto_associate_backends:
                    # Auto-associate backends (Apple, Google) should automatically
                    # link to existing accounts to prevent duplicate account creation.
                    #
                    # Race condition mitigation:
                    # If two concurrent requests arrive with the same email, one may
                    # create an inactive user. When the second request finds that user,
                    # we activate it here instead of creating a duplicate.
                    #
                    # NOTE: We must call associate_user() here (not in the standard
                    # pipeline location) because we need to prevent the pipeline from
                    # creating a new user. Returning {'user': user} would still create
                    # a duplicate user with the same email.

                    # Activate incomplete signups (User.is_active=False)
                    was_inactive = False
                    if not user.is_active:
                        was_inactive = True
                        # Use profile.activate() for proper activation handling:
                        # - Sets User.is_active=True
                        # - Sends welcome email (if configured)
                        # - Sends Slack notification: "{email} has activated their account"
                        user.profile.activate()

                    # Link the social auth account to the existing Django User
                    associate_user(backend, uid, user=user, social=None)

                    # Send additional notification for incomplete signups
                    # to distinguish social auth completions from normal activations
                    if was_inactive:
                        site_name = htk_setting('HTK_SITE_NAME')
                        notify(
                            f'*{user.email}* connected social auth '
                            f'({backend_name}) to complete signup on {site_name}',
                            use_messages=False,
                        )
                elif user.is_active:
                    # User exists with this email but backend is not auto-associate
                    # (e.g., Facebook, Fitbit, Strava, Withings)
                    # Redirect user to log in first before linking accounts
                    strategy.request.session[
                        SOCIAL_REGISTRATION_SETTING_EMAIL
                    ] = social_email
                    if user.has_usable_password():
                        # User has a password → require password login to link
                        url_name = htk_setting(
                            'HTK_ACCOUNTS_REGISTER_SOCIAL_LOGIN_URL_NAME'
                        )
                        response = redirect(url_name)
                    else:
                        # User has no password → require social auth login to link
                        url_name = htk_setting(
                            'HTK_ACCOUNTS_REGISTER_SOCIAL_ALREADY_LINKED_URL_NAME'
                        )
                        response = redirect(url_name)
                else:
                    # Edge case: inactive user trying to sign in with non-auto-associate backend
                    # Let the pipeline continue; downstream handlers will manage this case
                    pass
            else:
                # No existing user found with this email
                # Pipeline will continue to create a new user account
                pass

        elif collected_email:
            # email provided by user
            details['email'] = collected_email
            response = {'details': details}
        else:
            # no email provided from social auth
            strategy.request.session[
                SOCIAL_REGISTRATION_SETTING_MISSING_EMAIL
            ] = True
            url_name = htk_setting(
                'HTK_ACCOUNTS_REGISTER_SOCIAL_EMAIL_URL_NAME'
            )
            response = redirect(url_name)
    else:
        pass

    return response


@partial
def check_terms_agreement(strategy, details, user=None, *args, **kwargs):
    """
    Ask the user to agree to Privacy Policy and Terms of Service
    """
    response = None
    if user is None:
        agreed_to_terms = strategy.request.session.get(
            SOCIAL_REGISTRATION_SETTING_AGREED_TO_TERMS, False
        )
        if not agreed_to_terms:
            email = details.get('email')
            strategy.request.session[SOCIAL_REGISTRATION_SETTING_EMAIL] = email
            url_name = htk_setting(
                'HTK_ACCOUNTS_REGISTER_SOCIAL_EMAIL_AND_TERMS_URL_NAME'
            )
            response = redirect(url_name)
        else:
            pass
    else:
        pass
    return response


def check_incomplete_signup(strategy, details, user=None, *args, **kwargs):
    """Checks for an incomplete signup, and sets that User instead"""
    response = None
    if user is None:
        social_email = details.get('email')
        user = get_incomplete_signup_user_by_email(social_email)
        response = {
            'user': user,
            'is_new': user is None,
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
    """Associate email with the user"""
    if not user or not social:
        return None

    response = None

    email = details.get('email')
    domain = strategy.request.get_host()
    # Should confirm if the email was provided by the social auth provider, not the user
    # i.e. SOCIAL_REGISTRATION_SETTING_MISSING_EMAIL was False
    confirmed = not (
        strategy.request.session.get(
            SOCIAL_REGISTRATION_SETTING_MISSING_EMAIL, False
        )
    )
    user_email = associate_user_email(
        user, email, domain=domain, confirmed=confirmed
    )

    if user_email:
        # need to update the User with the activated one, so that it doesn't get
        # overwritten later on
        response = {
            'user': user_email.user,
        }
    return response


def handle_new_user(user, is_new, *args, **kwargs):
    """Do stuff if the account was newly created"""
    if not user:
        return None

    if is_new:
        # send a welcome email to the user, regardless of email confirmation status
        welcome_email(user)


def post_connect(user, social, *args, **kwargs):
    response = None
    return response
