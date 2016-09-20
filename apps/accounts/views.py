from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
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
from htk.apps.accounts.forms.auth import UpdatePasswordForm
from htk.apps.accounts.forms.auth import UserRegistrationForm
from htk.apps.accounts.forms.auth import UsernameEmailAuthenticationForm
from htk.apps.accounts.models import UserEmail
from htk.apps.accounts.session_keys import *
from htk.apps.accounts.utils import get_user_by_email
from htk.apps.accounts.utils.auth import login_authenticated_user
from htk.apps.accounts.view_helpers import redirect_to_social_auth_complete
from htk.forms.utils import set_input_attrs
from htk.utils import htk_setting
from htk.utils import utcnow
from htk.view_helpers import render_to_response_custom as _r
from htk.view_helpers import wrap_data

################################################################################
# login and logout

def login_view(
    request,
    data=None,
    auth_form_model=UsernameEmailAuthenticationForm,
    default_next_url_name='account_login_redirect',
    template='account/login.html',
    renderer=_r
):
    if data is None:
        data = wrap_data(request)
    data.update(csrf(request))
    success = False
    if request.method == 'POST':
        auth_form = auth_form_model(None, request.POST)
        if auth_form.is_valid():
            user = auth_form.get_user()
            login_authenticated_user(request, user)
            success = True
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
        auth_form = auth_form_model(None)

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

def register_social_email(
    request,
    data=None,
    template='account/register_social_email.html',
    renderer=_r
):
    from htk.apps.accounts.forms.auth import SocialRegistrationEmailForm

    if data is None:
        data = wrap_data(request)
    email = None
    success = False
    if request.method == 'POST':
        email_form = SocialRegistrationEmailForm(request.POST)
        if email_form.is_valid():
            email = email_form.save(request)
            success = True
        else:
            for error in email_form.non_field_errors():
                data['errors'].append(error)
    else:
        email_form = SocialRegistrationEmailForm(None)

    if success:
        user = get_user_by_email(email)
        if user:
            # a user is already associated with this email
            if user.has_usable_password():
                # user should log into the existing account with a password
                url_name = htk_setting('HTK_ACCOUNTS_REGISTER_SOCIAL_LOGIN_URL_NAME')
            else:
                # no password was set, so user must log in with another social auth account
                url_name = htk_setting('HTK_ACCOUNTS_REGISTER_SOCIAL_ALREADY_LINKED_URL_NAME')
            response = redirect(url_name)
        else:
            response = redirect_to_social_auth_complete(request)
    else:
        data['email_form'] = email_form
        response = _r(template, data)
    return response

def register_social_login(
    request,
    data=None,
    resend_confirmation_url_name='account_resend_confirmation',
    template='account/register_social_login.html',
    renderer=_r
):
    """For when a user is already associated with this email and has a usable password set
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
            login_authenticated_user(request, user)
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

def register_social_already_linked(
    request,
    data=None,
    template='account/register_social_login.html',
    renderer=_r
):
    """For when a user is already associated with this email only through social auth and no password set
    """
    if data is None:
        data = wrap_data(request)

    email = request.session.get(SOCIAL_REGISTRATION_SETTING_EMAIL)
    data['email'] = email
    response = renderer(template, data)
    return response

def register(
    request,
    data=None,
    reg_form_model=UserRegistrationForm,
    reg_form_kwargs=None,
    auth_form_model=UsernameEmailAuthenticationForm,
    success_url_name='account_register_done',
    login_if_success=False,
    template='account/register.html',
    email_template=None,
    email_subject=None,
    email_sender=None,    
    renderer=_r
):
    if data is None:
        data = wrap_data(request)

    data.update(csrf(request))
    success = False
    if request.method == 'POST':
        if reg_form_kwargs is None:
            reg_form_kwargs = {}
        reg_form = reg_form_model(request.POST, **reg_form_kwargs)
        if reg_form.is_valid():
            domain = request.get_host()
            new_user = reg_form.save(domain=domain, email_template=email_template, email_subject=email_subject, email_sender=email_sender)
            if login_if_success:
                username = new_user.username
                password = reg_form.cleaned_data.get('password1') # new_user.password is a hashed value
                auth_user = authenticate(username=username, password=password)
                login_authenticated_user(request, auth_user)
            else:
                pass
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
    if 'input_attrs' in data:
        set_input_attrs(resend_confirmation_form, attrs=data['input_attrs'])
    data['resend_confirmation_form'] = resend_confirmation_form
    response = renderer(template, data)
    return response

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
            for error in form.non_field_errors():
                data['errors'].append(error)
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
        UserModel = get_user_model()
        try:
            uid_int = base36_to_int(uidb36)
            user = UserModel.objects.get(id=uid_int)
        except (ValueError, UserModel.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            validlink = True
            if request.method == 'POST':
                form = UpdatePasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    success = True
            else:
                form = UpdatePasswordForm(None)
            if 'input_attrs' in data:
                set_input_attrs(form, attrs=data['input_attrs'])
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
