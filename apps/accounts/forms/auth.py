from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from htk.apps.accounts.utils import authenticate_user_by_username_email
from htk.apps.accounts.utils import email_to_username_hash
from htk.apps.accounts.utils import get_user_by_email
from htk.utils import htk_setting
from htk.apps.accounts.emails import password_reset_email
from htk.apps.accounts.session_keys import *

UserModel = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label=_('Email'))

    class Meta:
        model = UserModel
        fields = (
            'email',
        )

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        del self.fields['username']
        self.fields['password2'].label = 'Confirm Password'
        for name, field in self.fields.items():
            if field.widget.__class__ in (forms.TextInput, forms.PasswordInput,):
                field.widget.attrs['class'] = 'pure-input-1'
                field.widget.attrs['placeholder'] = field.label

    def clean_email(self):
        email = self.cleaned_data['email']

        user = get_user_by_email(email)
        if user is not None:
            self.email = None
            raise forms.ValidationError(_("A user with that email already exists."))
        else:
            self.email = email
        return email

    def save(self, domain=None, commit=True):
        domain = domain or htk_setting('HTK_DEFAULT_EMAIL_SENDING_DOMAIN')
        user = super(UserRegistrationForm, self).save(commit=False)
        email = self.email
        # temporarily assign a unique username so that we can create the record and the user can log in
        user.username = email_to_username_hash(email)
        # we'll store the primary email in the User object
        user.email = email
        user.primary_email = email
        # require user to confirm email account before activating it
        user.is_active = False
        if commit:
            user.save()
            user_email = associate_user_email(user, email, domain)
        return user

class ResendConfirmationForm(forms.Form):
    email = forms.EmailField(label='Email')

    def __init__(self, *args, **kwargs):
        super(ResendConfirmationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Email'

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            UserEmail.objects.get(email=email)
        except UserEmail.DoesNotExist:
            raise forms.ValidationError(_("A user with that email does not exist."))
        return email

class PasswordResetFormHtmlEmail(PasswordResetForm):
    """Modeled after django.contrib.auth.forms.PasswordResetForm
    """
    def clean(self):
        cleaned_data = self.cleaned_data
        email = self.cleaned_data['email']
        active_users = UserModel._default_manager.filter(
            email__iexact=email,
            is_active=True
        )
        self.active_users = active_users
        return cleaned_data

    def save(self,
             domain_override=None,
             subject_template_name='', # not used
             email_template_name='', # not used
             use_https=False,
             token_generator=default_token_generator,
             from_email=None,
             request=None):
        """Generates a one-use only link for resetting password and sends to the user
        """
        domain = request.get_host()
        for user in self.active_users:
            password_reset_email(
                user,
                token_generator,
                use_https=use_https,
                domain=domain
            )

class UsernameEmailAuthenticationForm(forms.Form):
    """Based on django.contrib.auth.forms.AuthenticationForm
    """
    username_email = forms.CharField(label=_('Username or Email'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter the correct credentials. Note that password is case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(UsernameEmailAuthenticationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.__class__ in (forms.TextInput, forms.PasswordInput,):
                field.widget.attrs['class'] = 'pure-input-1'
                field.widget.attrs['placeholder'] = field.label

    def clean(self, username_email=None, password=None):
        """Clean the form and try to get user
        Parameterize username_email and password to allow invoking from subclass
        """
        if not username_email:
            username_email = self.cleaned_data.get('username_email')
        if not password:
            password = self.cleaned_data.get('password')

        if username_email and password:
            self.user_cache = authenticate_user_by_username_email(username_email, password)
        else:
            self.user_cache = None

        if self.user_cache is None:
            raise forms.ValidationError(self.error_messages['invalid_login'])
        elif not self.user_cache.is_active:
            raise forms.ValidationError(self.error_messages['inactive'])
        else:
            # all good, do nothing
            pass

        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

################################################################################
# Social registration

class SocialRegistrationEmailForm(forms.Form):
    email = forms.EmailField(label='Email')

    def __init__(self, *args, **kwargs):
        super(SocialRegistrationEmailForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.__class__ in (forms.TextInput, forms.PasswordInput,):
                field.widget.attrs['class'] = 'pure-input-1'
                field.widget.attrs['placeholder'] = field.label

    def clean_email(self):
        email = self.cleaned_data['email']
        self.email = email
        return email

    def save(self, request):
        email = self.email
        request.session[SOCIAL_REGISTRATION_SETTING_EMAIL] = email
        return email

class SocialRegistrationAuthenticationForm(UsernameEmailAuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, email, *args, **kwargs):
        super(SocialRegistrationAuthenticationForm, self).__init__(None, *args, **kwargs)
        del self.fields['username_email']
        self.email = email

    def clean(self):
        email = self.email
        password = self.cleaned_data.get('password')
        return super(SocialRegistrationAuthenticationForm, self).clean(username_email=email, password=password)
