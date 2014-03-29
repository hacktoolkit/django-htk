import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

from htk.api.constants import *
from htk.api.utils import json_response
from htk.api.utils import json_response
from htk.api.utils import json_response_error
from htk.api.utils import json_response_error
from htk.api.utils import json_response_okay
from htk.api.utils import json_response_okay
from htk.apps.accounts.enums import ProfileAvatarType
from htk.apps.accounts.forms.update import ChangePasswordForm
from htk.apps.accounts.utils import resolve_encrypted_uid
from htk.forms.utils import get_form_errors

##################################################
# Read API views

@login_required
def suggest(request):
    """This API endpoint supports User autocomplete

    TODO:
    First retrieve from followers and following, then search all users
    """
    UserModel = get_user_model()
    query = request.GET.get('q')
    if query:
        query = query.strip()
        user_results = UserModel.objects.filter(username__istartswith=query)
        results = [
            {
                'username' : user.username,
            }
            for user in user_results
        ]
        obj = {
            'data' : {
                'results' : results,
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

@login_required
@require_POST
def password(request):
    """Update a User's password
    """
    user = request.user
    password_form = ChangePasswordForm(user, request.POST)
    if password_form.is_valid():
        password_form.save()
        response = json_response_okay()
    else:
        response = json_response_error()
    return response

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
