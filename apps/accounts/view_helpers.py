# Django Imports
from django.shortcuts import redirect
from django.utils.safestring import mark_safe

# HTK Imports
from htk.apps.accounts.constants.social import SOCIAL_AUTHS
# from htk.apps.accounts.session_keys import SOCIAL_AUTH_PARTIAL_PIPELINE_KEY
from htk.utils import htk_setting
from htk.utils.urls import reverse_with_query_params


def get_social_auth_providers():
    providers = set(htk_setting('HTK_SOCIAL_AUTH_PROVIDERS'))
    social_auth_providers = [
        social_auth
        for social_auth in SOCIAL_AUTHS
        if social_auth.provider in providers
    ]
    return social_auth_providers


def get_social_auths_statuses(user=None):
    """Get the statuses of all social auths for a user"""
    connected_social_auths = set(
        user.profile.get_social_auths().values_list('provider', flat=True)
        if user
        else []
    )

    providers = set(htk_setting('HTK_SOCIAL_AUTH_PROVIDERS'))
    statuses = [
        social_auth.with_status(
            connected=social_auth.provider in connected_social_auths
        )
        for social_auth in SOCIAL_AUTHS
        if social_auth.provider in providers
    ]

    return statuses


def redirect_to_social_auth_complete(request):
    """Return an HTTP Redirect response to social:complete to continue the pipeline"""
    backend = request.session['backend']
    # backend = request.session[SOCIAL_AUTH_PARTIAL_PIPELINE_KEY]['backend']
    response = redirect('social:complete', backend=backend)
    return response


def get_resend_confirmation_help_message(
    resend_confirmation_url_name, email=None
):
    query_params = {
        'email': email,
    }
    resend_confirmation_url = reverse_with_query_params(
        resend_confirmation_url_name, query_params
    )
    msg = (
        'Have you confirmed your email address yet? <a id="resend_confirmation" href="%s">Request another confirmation email</a>.'
        % resend_confirmation_url
    )
    return mark_safe(msg)
