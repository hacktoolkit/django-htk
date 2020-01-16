# Python Standard Library Imports
import json

# Django Imports
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

# HTK Imports
from htk.api.constants import *
from htk.api.utils import json_response
from htk.api.utils import json_response_error
from htk.api.utils import json_response_okay
from htk.apps.accounts.enums import ProfileAvatarType
from htk.apps.accounts.forms.settings import AddEmailForm
from htk.apps.accounts.forms.update import ChangePasswordForm
from htk.apps.accounts.forms.update import ChangeUsernameForm
from htk.apps.accounts.models import UserEmail
from htk.apps.accounts.utils import resolve_encrypted_uid
from htk.apps.accounts.utils.auth import login_authenticated_user
from htk.forms.utils import get_form_error
from htk.forms.utils import get_form_errors
from htk.utils import htk_setting


##################################################
# Authentication API views

@require_POST
def login_view(request):
    from htk.apps.accounts.forms.auth import UsernameEmailAuthenticationForm
    auth_form = UsernameEmailAuthenticationForm(None, request.POST)
    if auth_form.is_valid():
        user = auth_form.get_user()
        login_authenticated_user(request, user)
        response = json_response_okay()
    else:
        response = json_response_error()
    return response

def logout_view(request):
    logout(request)
    reponse = json_response_okay()
    return response

##################################################
# Read API views

@login_required
def suggest(request):
    """This API endpoint supports User autocomplete
    """
    from htk.apps.accounts.formatters import DEFAULT_USER_SUGGEST_FORMATTER
    from htk.apps.accounts.search import search_by_username_name
    query = request.GET.get('q')
    if query:
        query = query.strip()
        user_results = search_by_username_name(query)
        formatted_results = [DEFAULT_USER_SUGGEST_FORMATTER(user) for user in user_results]
        obj = {
            'data' : {
                'results' : formatted_results,
            },
        }
        response = json_response(obj)
    else:
        response = json_response_error()
    return response

##################################################
# Write API views
# Various views for updating User and UserProfile state

@login_required
@require_POST
def update(request):
    """Updates a User or UserProfile

    It is important to note that UserUpdateForm only updates the fields on User and UserProfile that are passed in, and does not have to update the entire object
    """
    user = request.user
    from htk.apps.accounts.forms.update import UserUpdateForm
    user_update_form = UserUpdateForm(user, request.POST)
    user_profile_update_form = user_update_form.get_profile_form()
    if user_update_form.is_valid() and user_profile_update_form.is_valid():
        updated_user = user_update_form.save()
        updated_profile = user_profile_update_form.save()
        response = json_response_okay()
    else:
        (errors, field_errors,) = get_form_errors(user_update_form)
        (profile_errors, profile_field_errors,) = get_form_errors(user_profile_update_form)
        obj = {
            HTK_API_JSON_KEY_STATUS: HTK_API_JSON_VALUE_ERROR,
            'errors' : errors + profile_errors,
            'field_errors' : field_errors + profile_field_errors,
        }
        response = json_response(obj)
    return response

@login_required
@require_POST
def username(request):
    """Update a User's username
    """
    user = request.user
    username_form = ChangeUsernameForm(user, request.POST)
    if username_form.is_valid():
        username_form.save(user)
        response = json_response_okay()
    else:
        obj = {
            HTK_API_JSON_KEY_STATUS: HTK_API_JSON_VALUE_ERROR,
            'error' : get_form_error(username_form)
        }
        response = json_response(obj)
    return response

@login_required
@require_POST
def password(request):
    """Update a User's password
    """
    user = request.user
    password_form = ChangePasswordForm(user, request.POST)
    if password_form.is_valid():
        user = password_form.save(user)
        if htk_setting('HTK_ACCOUNTS_CHANGE_PASSWORD_UPDATE_SESSION_AUTH_HASH'):
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
        response = json_response_okay()
    else:
        response = json_response_error()
    return response

@login_required
@require_POST
def avatar(request):
    """Update a User's avatar to the specified type
    """
    json_data = json.loads(request.body)

    avatar_type_name = json_data['type']
    if avatar_type_name in ProfileAvatarType.__members__:
        user = request.user
        profile = user.profile
        profile.avatar = ProfileAvatarType[avatar_type_name].value
        profile.save(update_fields=['avatar',])
        response = json_response_okay()
    else:
        response = json_response_error()

    return response

@require_POST
@login_required
def follow(request, encrypted_uid):
    """Follow another user
    """
    user = request.user
    other_user = resolve_encrypted_uid(encrypted_uid)
    if other_user:
        user.profile.follow_user(other_user)
        response = json_response_okay()
    else:
        response = json_response_error()
    return response

@require_POST
@login_required
def unfollow(request, encrypted_uid):
    """Unfollow another user
    """
    user = request.user
    other_user = resolve_encrypted_uid(encrypted_uid)
    if other_user:
        user.profile.unfollow_user(other_user)
        response = json_response_okay()
    else:
        response = json_response_error()
    return response

##################################################
# Emails

@require_POST
@login_required
def email_add(request):
    user = request.user
    add_email_form = AddEmailForm(user, request.POST)
    if add_email_form.is_valid():
        domain = request.get_host()
        user_email = add_email_form.save(domain=domain)
        response = json_response_okay()
    else:
        errors = []
        for error in add_email_form.non_field_errors():
            errors.append(error)
        obj = {
            HTK_API_JSON_KEY_STATUS: HTK_API_JSON_VALUE_ERROR,
            'errors': errors,
        }
        response = json_response(obj)
    return response

@require_POST
@login_required
def email_set_primary(request):
    user = request.user
    email = request.POST.get('email')
    user_email = get_object_or_404(UserEmail, user=user, email=email)
    user = user_email.set_primary_email()
    if user:
        response = json_response_okay()
    else:
        response = json_response_error()
    return response

@require_POST
@login_required
def email_delete(request):
    user = request.user
    email = request.POST.get('email')

    if user.profile.is_company_employee:
        # admin user, grab only by email
        user_email = get_object_or_404(UserEmail, email=email)
    else:
        # regular user, retrieve by user and email
        from htk.apps.accounts.utils import get_user_email
        user_email = get_user_email(user, email)

    if user_email:
        if user_email.delete():
            response = json_response_okay()
        else:
            response = json_response_error()
    else:
        # email does not exist or was already deleted
        response = json_response_okay()

    return response
