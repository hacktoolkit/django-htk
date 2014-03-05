from django.conf import settings

import htk.apps.accounts.forms.update as update_forms
from htk.apps.accounts.models import AbstractUserProfile
from htk.utils import resolve_model_dynamically

UserProfile = resolve_model_dynamically(settings.AUTH_PROFILE_MODULE)

USER_UPDATE_FORMS = {
    'update_username_form' : update_forms.UpdateUsernameForm,
    'update_user_first_name_form' : update_forms.UpdateUserFirstNameForm,
    'update_user_last_name_form' : update_forms.UpdateUserLastNameForm,
}

if issubclass(AbstractUserProfile, UserProfile):
    USER_UPDATE_FORMS.update({
            'update_user_share_name_form' : update_forms.UpdateUserShareNameForm,
            'update_user_website_form' : update_forms.UpdateUserWebsiteForm,
            'update_user_facebook_form' : update_forms.UpdateUserFacebookForm,
            'update_user_twitter_form' : update_forms.UpdateUserTwitterForm,
            'update_user_city_form' : update_forms.UpdateUserCityForm,
            'update_user_state_form' : update_forms.UpdateUserStateForm,
            'update_user_share_location_form' : update_forms.UpdateUserShareLocationForm,
            'update_user_biography_form' : update_forms.UpdateUserBiographyForm,
    })
else:
    pass

def get_user_update_form(request):
    update_type = request.POST.get('update_form_type', False)
    update_form = None
    for form_type in USER_UPDATE_FORMS:
        if form_type == update_type:
            update_form = USER_UPDATE_FORMS[form_type]
            break
    return update_form
