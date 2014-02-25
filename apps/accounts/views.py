from django.contrib.auth import authenticate
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import logout
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import password_reset
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.http import base36_to_int
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from htk.apps.accounts.decorators import logout_required
from htk.apps.accounts.exceptions import NonUniqueEmail
from htk.apps.accounts.forms.auth import ResendConfirmationForm
from htk.apps.accounts.forms.auth import UserRegistrationForm
from htk.apps.accounts.forms.auth import UsernameEmailAuthenticationForm
from htk.apps.accounts.models import UserEmail
from htk.apps.accounts.session_keys import *
from htk.apps.accounts.view_helpers import redirect_to_social_auth_complete
from htk.utils import utcnow
from htk.view_helpers import render_to_response_custom as _r
from htk.view_helpers import wrap_data

UserModel = get_user_model()

################################################################################
# login and logout

def login_view(
    request,
    data=None,
    default_next_url_name='account_login_redirect',
    template='account/login.html',
    renderer=_r
):
    if data is None:
        data = wrap_data(request)
    data.update(csrf(request))
    success = False
    if request.method == 'POST':
        auth_form = UsernameEmailAuthenticationForm(None, request.POST)
        if auth_form.is_valid():
            user = auth_form.get_user()
            login(request, user)
            success = True
            user.profile.update_locale_info_by_ip_from_request(request)
            default_next_uri = reverse(default_next_url_name)
            next_uri = request.GET.get('next', default_next_uri)
        else:
            for error in auth_form.non_field_errors():
                data['errors'].append(error)
            auth_user = auth_form.get_user()
            if auth_user and not auth_user.is_active:
                data['errors'].append('Have you confirmed your email address yet? <a id="resend_confirmation" href="javascript:void(0);">Resend confirmation &gt;</a>')
                resend_confirmation_form = ResendConfirmationForm({'email': auth_user.email})
                data['resend_confirmation_form'] = resend_confirmation_form
            else:
                pass
    else:
        auth_form = UsernameEmailAuthenticationForm(None)

    if success:
        response = redirect(next_uri)
    else:
        data['auth_form'] = auth_form
        response = renderer(template, data)

    return response

def logout_view(
    request,
    redirect_url_name='home',
    *args,
    **kwargs
):
    logout(request)
    response = redirect(redirect_url_name, *args)
    return response

################################################################################
# registration and activation

def register_social_login(
    request,
    data=None,
    resend_confirmation_url_name='account_resend_confirmation',
    template='account/register_social_login.html',
    renderer=_r
):
    """For when a user is already associated with this email
    """
    from htk.apps.accounts.forms.auth import SocialRegistrationAuthenticationForm

    if data is None:
        data = wrap_data(request)

    email = request.session.get(SOCIAL_REGISTRATION_SETTING_EMAIL)
    data['email'] = email
    data.update(csrf(request))

    success = False
    if request.method == 'POST':
        auth_form = SocialRegistrationAuthenticationForm(email, request.POST)
        if auth_form.is_valid():
            user = auth_form.get_user()
            login(request, user)
            success = True
        else:
            for error in auth_form.non_field_errors():
                data['errors'].append(error)
            auth_user = auth_form.get_user()
            if auth_user and not auth_user.is_active:
                data['errors'].append('Have you confirmed your email address yet? <a href="%s">Resend confirmation</a>.' % reverse(resend_confirmation_url_name))
    else:
        auth_form = SocialRegistrationAuthenticationForm(email)

    if success:
        response = redirect_to_social_auth_complete(request)
    else:
        data['auth_form'] = auth_form
        response = renderer(template, data)
    return response

def register(
    request,
    data=None,
    reg_form_model=UserRegistrationForm,
    auth_form_model=UsernameEmailAuthenticationForm,
    success_url_name='account_register_done',
    template='account/register.html',
    renderer=_r
):
    if data is None:
        data = wrap_data(request)

    data.update(csrf(request))
    success = False
    if request.method == 'POST':
        reg_form = reg_form_model(request.POST)
        if reg_form.is_valid():
            domain = request.get_host()
            new_user = reg_form.save(domain)
            # if we did want to log the user in right away, this is what we'd do... but we don't want to do it
            #username = user.username
            #password = reg_form.cleaned_data.get('password1') # user.password is a hashed value
            #auth_user = authenticate(username=username, password=password)
            #login(request, auth_user)
            success = True
        else:
            for error in reg_form.non_field_errors():
                data['errors'].append(error)
            # might be tempted to do this, but it might display too many errors/multiple errors per field
            # so we will just handle it in the form's clean() method
            #for error in reg_form._errors.values():
                #data['errors'].append(error)
    else:
        reg_form = reg_form_model(None)
    data['reg_form'] = reg_form
    if auth_form_model:
        # register page also has an auth form
        auth_form = auth_form_model(None)
        data['auth_form'] = auth_form
    if success:
        response = redirect(reverse(success_url_name))
    else:
        response = renderer(template, data)
    return response

def register_done(
    request,
    data=None,
    template='account/register_done.html',
    renderer=_r
):
    if data is None:
        data = wrap_data(request)

    response = renderer(template, data)
    return response

def resend_confirmation(
    request,
    data=None,
    template='account/resend_confirmation.html',
    renderer=_r
):
    if data is None:
        data = wrap_data(request)

    data.update(csrf(request))
    if request.method == 'POST':
        resend_confirmation_form = ResendConfirmationForm(request.POST)
        if resend_confirmation_form.is_valid():
            email = resend_confirmation_form.cleaned_data.get('email')
            user_emails = UserEmail.objects.filter(email=email)
            num_confirmed_user_emails = user_emails.filter(is_confirmed=True).count()
            if num_confirmed_user_emails == 1:
                data['already_active'] = True
            elif num_confirmed_user_emails > 1:
                raise NonUniqueEmail(email)
            else:
                unconfirmed_user_emails = user_emails.filter(is_confirmed=False)
                for unconfirmed in unconfirmed_user_emails:
                    unconfirmed.send_activation_email(domain=request.get_host(), resend=True)
                data['success'] = True
        else:
            for error in resend_confirmation_form.non_field_errors():
                data['errors'].append(error)
    else:
        resend_confirmation_form = ResendConfirmationForm()
    data['resend_confirmation_form'] = resend_confirmation_form
    return renderer(template, data)

@require_GET
def confirm_email(
    request,
    activation_key,
    data=None,
    resend_confirmation_url_name='account_resend_confirmation',
    template='account/confirm_email.html',
    renderer=_r
):
    if data is None:
        data = wrap_data(request)

    user = request.user
    user_email = get_object_or_404(UserEmail,
                                   activation_key=activation_key)
    if user and user != user_email.user:
        # for a mismatched user, force logout
        logout(request)
        user = None
        data['user'] = None

    # attempt to confirm
    if user_email.key_expires < utcnow():
        data['expired'] = True
        data['resend_confirmation_uri'] = reverse(resend_confirmation_url_name)
    else:
        was_activated = user_email.confirm_and_activate_account()
        data['was_activated'] = was_activated
        data['success'] = True

    response = renderer(template, data)
    return response

########################################################################
# password reset

def forgot_password(
    request,
    data=None,
    redirect_url_name='account_password_reset_done',
    template='account/forgot_password.html',
    renderer=_r
):
    """Modeled after django.contrib.auth.views.password_reset
    """
    from htk.apps.accounts.forms.auth import PasswordResetFormHtmlEmail

    if data is None:
        wrap_data(request)

    data.update(csrf(request))
    if request.method == 'POST':
        form = PasswordResetFormHtmlEmail(request.POST)
        if form.is_valid():
            opts = {
                'request': request,
            }
            form.save(**opts)
            response = redirect(redirect_url_name)
        else:
            if hasattr(form, 'users_cache') and len(form.users_cache) > 0 and not any(user.is_active for user in form.users_cache):
                # users_cache non-empty but inactive users
                data['errors'].append("That account is not active yet because you haven't confirmed your email. <a id=\"resend_confirmation\" href=\"javascript:void(0);\">Resend email confirmation &gt;</a>")
                # remove the field error
                del form._errors['email']
            else:
                # no users found, or users with unusable password
                pass
            data['form'] = form
            response = renderer(template, data)
    else:
        form = PasswordResetFormHtmlEmail()
        data['form'] = form
        response = renderer(template, data)
    return response

def password_reset_done(
    request,
    data=None,
    template='account/password_reset_done.html',
    renderer=_r
):
    if data is None:
        data = wrap_data(request)

    response = renderer(template, data)
    return response

# Doesn't need csrf_protect since no one can guess the URL
@csrf_exempt
@logout_required
def reset_password(
    request,
    data=None,
    redirect_url_name='account_password_reset_success',
    template='account/reset_password.html',
    renderer=_r
):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    Based off of django.contrib.auth.views.password_reset_confirm
    Need to customize error display
    """
    if data is None:
        data = wrap_data(request)

    uidb36 = request.GET.get('u', None)
    token = request.GET.get('t', None)
    token_generator = default_token_generator
    success = False
    response = None
    if uidb36 and token:
        try:
            uid_int = base36_to_int(uidb36)
            user = UserModel.objects.get(id=uid_int)
        except (ValueError, UserModel.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            validlink = True
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    success = True
            else:
                form = SetPasswordForm(None)
        else:
            validlink = False
            form = None
        data['form'] = form
        data['validlink'] = validlink
    else:
        data['validlink'] = False
    if success:
        response = redirect(reverse(redirect_url_name))
    else:
        response = renderer(template, data)
    return response

def password_reset_success(
    request,
    data=None,
    template='account/password_reset_success.html',
    renderer=_r
):
    if data is None:
        data = wrap_data(request)

    response = renderer(template, data)
    return response
