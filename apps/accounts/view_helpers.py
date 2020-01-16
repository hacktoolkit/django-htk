# Django Imports
from django.shortcuts import redirect
from django.utils.safestring import mark_safe

# HTK Imports
from htk.apps.accounts.constants import *
from htk.apps.accounts.session_keys import *
from htk.utils.urls import reverse_with_query_params


def get_social_auths_status(user):
    user_social_auths = user.profile.get_social_auths()
    status_dict = {}
    for social_auth in user_social_auths:
        status_dict[social_auth.provider] = True

    status_list = []
    for social_auth in SOCIAL_AUTHS:
        key = social_auth['key']
        name = social_auth['name']
        item = {
            'key' : key,
            'name' : name,
            'linked' : status_dict.get(key, False)
        }
        status_list.append(item)
    return status_list

def redirect_to_social_auth_complete(request):
    """Return an HTTP Redirect response to social:complete to continue the pipeline
    """
    backend = request.session['backend']
    #backend = request.session[SOCIAL_AUTH_PARTIAL_PIPELINE_KEY]['backend']
    response = redirect('social:complete', backend=backend)
    return response

def get_resend_confirmation_help_message(resend_confirmation_url_name, email=None):
    query_params = {
        'email' : email,
    }
    resend_confirmation_url = reverse_with_query_params(resend_confirmation_url_name, query_params)
    msg = 'Have you confirmed your email address yet? <a id="resend_confirmation" href="%s">Request another confirmation email</a>.' % resend_confirmation_url
    return mark_safe(msg)
