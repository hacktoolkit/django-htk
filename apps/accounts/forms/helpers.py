from htk.apps.accounts.forms.update import UpdateUserBiographyForm
from htk.apps.accounts.forms.update import UpdateUserCityForm
from htk.apps.accounts.forms.update import UpdateUserFacebookForm
from htk.apps.accounts.forms.update import UpdateUserFirstNameForm
from htk.apps.accounts.forms.update import UpdateUserLastNameForm
from htk.apps.accounts.forms.update import UpdateUserShareLocationForm
from htk.apps.accounts.forms.update import UpdateUserShareNameForm
from htk.apps.accounts.forms.update import UpdateUserStateForm
from htk.apps.accounts.forms.update import UpdateUserTwitterForm
from htk.apps.accounts.forms.update import UpdateUserWebsiteForm
from htk.apps.accounts.forms.update import UpdateUsernameForm

USER_UPDATE_FORMS = {
    'update_username_form' : UpdateUsernameForm,
    'update_user_first_name_form' : UpdateUserFirstNameForm,
    'update_user_last_name_form' : UpdateUserLastNameForm,
    'update_user_share_name_form' : UpdateUserShareNameForm,
    'update_user_website_form' : UpdateUserWebsiteForm,
    'update_user_facebook_form' : UpdateUserFacebookForm,
    'update_user_twitter_form' : UpdateUserTwitterForm,
    'update_user_city_form' : UpdateUserCityForm,
    'update_user_state_form' : UpdateUserStateForm,
    'update_user_share_location_form' : UpdateUserShareLocationForm,
    'update_user_biography_form' : UpdateUserBiographyForm,
    }

def get_user_update_form(request):
    update_type = request.POST.get('update_form_type', False)
    update_form = None
    for form_type in USER_UPDATE_FORMS:
        if form_type == update_type:
            update_form = USER_UPDATE_FORMS[form_type]
            break
    return update_form
