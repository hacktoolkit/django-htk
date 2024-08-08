# Python Standard Library Imports

# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse


try:
    # Django 3.x
    # Django Imports
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    # Django 4.x
    from django.utils.translation import gettext_lazy as _


# HTK Imports
from htk.apps.accounts.emails import password_reset_email
from htk.apps.accounts.models import UserEmail
from htk.apps.accounts.session_keys import (
    SOCIAL_REGISTRATION_SETTING_AGREED_TO_TERMS,
    SOCIAL_REGISTRATION_SETTING_EMAIL,
)
from htk.apps.accounts.utils import (
    authenticate_user_by_username_email,
    email_to_username_hash,
    email_to_username_pretty_unique,
    get_user_by_email,
    get_user_by_email_with_retries,
)
from htk.forms.utils import (
    set_input_attrs,
    set_input_placeholder_labels,
)
from htk.utils import htk_setting
from htk.utils.request import get_current_request


UserModel = get_user_model()


# isort: off


class UpdatePasswordForm(SetPasswordForm):
    """A subclass of Django's SetPasswordForm
    Sends out a password_changed_email
    """

    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        set_input_placeholder_labels(self)
        set_input_attrs(self)

    def save(self, commit=True, email_template=None):
        user = super(UpdatePasswordForm, self).save(commit=commit)
        from htk.apps.accounts.emails import password_changed_email

        try:
            password_changed_email(user)
        except Exception:
            request = get_current_request()
            rollbar.report_exc_info(request=request)
        return user


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label=_('Email'))
    recaptcha = forms.CharField(required=False, widget=forms.HiddenInput)

    error_messages = {
        'duplicate_username': _('A user with that username already exists.'),
        'password_mismatch': _("The two password fields didn't match."),
        'email_already_associated': _(
            'That email is already associated with a %s account. If you are trying to login to an existing account, click the "Login" button.' % htk_setting('HTK_SITE_NAME')  # noqa
         ),
        'invalid_email': _('Invalid email. Please enter a valid email.'),
        'empty_password': _("The password can't be empty."),
    }

    class Meta:
        model = UserModel
        fields = (
            'email',
        )

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.cascaded_errors = []
        if 'username' in self.fields:
            del self.fields['username']
        self.fields['password2'].label = 'Confirm Password'
        self.label_suffix = ''
        set_input_attrs(self)
        set_input_placeholder_labels(self)

    def clean(self):
        """We are using cascaded_errors to bubble up any field-level errors to form-wide
        """
        cleaned_data = super(UserRegistrationForm, self).clean()
        if 'email' in self._errors:
            # display all the errors at once?
            # raise forms.ValidationError()
            email_error = self._errors['email']
            if email_error[0] == self.error_messages['email_already_associated']:
                # email already associated
                self.cascaded_errors.append(self.error_messages['email_already_associated'])
            else:
                # generic invalid email
                self.cascaded_errors.append(self.error_messages['invalid_email'])
        # TODO: see clean_password1
        if 'password1' in self._errors:
            self.cascaded_errors.append(self._errors['password1'][0])
        if 'password2' in self._errors:
            self.cascaded_errors.append(self._errors['password2'][0])
            # syndicate error to first password field also, so that it would get the error styling
            self._errors['password1'] = [self._errors['password2'][0]]

        if len(self.cascaded_errors) > 0:
            raise forms.ValidationError(self.cascaded_errors)

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        from htk.utils.emails import normalize_email
        email = normalize_email(email)
        self.cleaned_data['email'] = email

        user = get_user_by_email(email)
        if user is not None:
            self.email = None
            raise forms.ValidationError(self.error_messages['email_already_associated'])
        else:
            self.email = email
        return email

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1 == '':
            raise forms.ValidationError(self.error_messages['empty_password'])
        return password1

    def save(self, domain=None, email_template=None, email_subject=None, email_sender=None, commit=True):
        """Handles a possible race condition and performs save
        """
        def _process_registration(self, domain, email_template, email_subject, email_sender, commit):
            domain = domain or htk_setting('HTK_DEFAULT_EMAIL_SENDING_DOMAIN')
            user = super(UserRegistrationForm, self).save(commit=False)
            # temporarily assign a unique username so that we can create the record and the user can log in
            if htk_setting('HTK_ACCOUNTS_REGISTER_SET_PRETTY_USERNAME_FROM_EMAIL', False):
                user.username = email_to_username_pretty_unique(email)
            else:
                user.username = email_to_username_hash(email)
            # we'll store the primary email in the User object
            user.email = email
            if not htk_setting('HTK_ACCOUNT_ACTIVATE_UPON_REGISTRATION', False):
                # require user to confirm email account before activating it
                user.is_active = False
            if commit:
                user.save()
                from htk.apps.accounts.utils import associate_user_email
                associate_user_email(
                    user,
                    email,
                    domain=domain,
                    email_template=email_template,
                    email_subject=email_subject,
                    email_sender=email_sender
                )
            return user

        from htk.apps.accounts.locks import UserEmailRegistrationLock
        email = self.email
        lock = UserEmailRegistrationLock(email)
        if lock.is_locked():
            # another user registration is in progress
            user = get_user_by_email_with_retries(email)
        else:
            try:
                lock.acquire()
                user = _process_registration(self, domain, email_template, email_subject, email_sender, commit)
            except Exception:
                rollbar.report_exc_info()
                # another user registration is in progress
                user = get_user_by_email_with_retries(email)
            finally:
                lock.release()
        return user


class NameEmailUserRegistrationForm(UserRegistrationForm):
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = (
            'first_name',
            'last_name',
            'email',
        )

    def __init__(self, *args, **kwargs):
        super(NameEmailUserRegistrationForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        set_input_attrs(self)
        set_input_placeholder_labels(self)

    def save(self, domain=None, email_template=None, email_subject=None, email_sender=None, commit=True):
        domain = domain or htk_setting('HTK_DEFAULT_EMAIL_SENDING_DOMAIN')
        user = super(NameEmailUserRegistrationForm, self).save(commit=False)
        email = self.email
        # temporarily assign a unique username so that we can create the record and the user can log in
        if htk_setting('HTK_ACCOUNTS_REGISTER_SET_PRETTY_USERNAME_FROM_EMAIL', False):
            user.username = email_to_username_pretty_unique(email)
        else:
            user.username = email_to_username_hash(email)
        # password1 = self.cleaned_data.get('password1')
        # user.set_password(password1)
        if commit:
            user.save()
            # associate user and email
            from htk.apps.accounts.utils import associate_user_email
            associate_user_email(
                user,
                email,
                domain=domain,
                email_template=email_template,
                email_subject=email_subject,
                email_sender=email_sender
            )
            # mark has_username_set
            user_profile = user.profile
            user_profile.has_username_set = True
            user_profile.save()

            # send welcome email
            was_activated = user.is_active
            if was_activated:
                user_profile.send_welcome_email()
        return user


class ResendConfirmationForm(forms.Form):
    email = forms.EmailField(label='Email')

    def __init__(self, *args, **kwargs):
        super(ResendConfirmationForm, self).__init__(*args, **kwargs)
        set_input_attrs(self)
        set_input_placeholder_labels(self)

    def clean_email(self):
        email = self.cleaned_data['email']
        user_emails = UserEmail.objects.filter(email=email)
        if not user_emails.exists():
            raise forms.ValidationError(_("A user with that email does not exist."))
        return email


class PasswordResetFormHtmlEmail(PasswordResetForm):
    """Modeled after django.contrib.auth.forms.PasswordResetForm
    """
    def __init__(self, *args, **kwargs):
        super(PasswordResetFormHtmlEmail, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        set_input_attrs(self)
        set_input_placeholder_labels(self)

    def clean(self):
        cleaned_data = self.cleaned_data
        email = self.cleaned_data.get('email', None)
        if email:
            user = get_user_by_email(email)
            if user:
                if user.is_active:
                    pass
                else:
                    self.inactive_user = True
                    raise forms.ValidationError(
                        "That account is not active yet because you haven't confirmed your email. <a id=\"resend_confirmation\" href=\"{}\">Resend email confirmation &gt;</a>".format(  # noqa
                            reverse(htk_setting('HTK_ACCOUNTS_RESEND_CONFIRMATION'))
                        )
                    )
        else:
            user = None

        if user is None:
            raise forms.ValidationError(
                "That email address doesn't have an associated user account. Are you sure you've registered?"  # noqa
            )
        else:
            self.user_cache = user
        return cleaned_data

    def save(
        self,
        domain_override=None,
        email_template=None,
        email_subject=None,
        email_sender=None,
        subject_template_name='',  # not used
        email_template_name='',  # not used
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None
    ):
        """Generates a one-use only link for resetting password and sends to the user
        """
        domain = request.get_host()
        password_reset_email(
            self.user_cache,
            token_generator,
            use_https=use_https,
            domain=domain,
            template=email_template,
            subject=email_subject,
            sender=email_sender
        )


class UsernameEmailAuthenticationForm(forms.Form):
    """Based on django.contrib.auth.forms.AuthenticationForm
    """
    username_email = forms.CharField(label=_('Username or Email'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    recaptcha = forms.CharField(required=False, widget=forms.HiddenInput)

    error_messages = {
        'invalid_login': _('Please enter a correct %(username_email)s and %(password)s. Note that password is case-sensitive.'),  # noqa
        'invalid_password': _('Please enter a correct %(password)s. Note that password is case-sensitive.'),
        'inactive': _('This account is inactive.'),
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
        set_input_attrs(self)
        set_input_placeholder_labels(self)

    def clean(self, username_email=None, password=None):
        """Clean the form and try to get user
        Parameterize username_email and password to allow invoking from subclass
        """
        if not username_email:
            username_email = self.cleaned_data.get('username_email', '').strip()
        if not password:
            password = self.cleaned_data.get('password')

        if username_email and password:
            self.user_cache = authenticate_user_by_username_email(self.request, username_email, password)
        else:
            self.user_cache = None

        if self.user_cache is None:
            if 'username_email' in self.fields:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={
                        'username_email': self.fields['username_email'].label,
                        'password': self.fields['password'].label,
                    },
                )
            else:
                raise forms.ValidationError(
                    self.error_messages['invalid_password'],
                    code='invalid_password',
                    params={
                        'password': self.fields['password'].label,
                    },
                )
        elif not self.user_cache.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
        else:
            # all good, do nothing
            pass

        return self.cleaned_data

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
        self.label_suffix = ''
        set_input_attrs(self)
        set_input_placeholder_labels(self)
        self.cascaded_errors = []

    def clean(self):
        """We are using cascaded_errors to bubble up any field-level errors to form-wide
        """
        cleaned_data = self.cleaned_data
        for field_name in self.fields:
            if field_name in self._errors:
                errors = self._errors[field_name]
                error_msg = errors[0]
                if error_msg == 'This field is required.':
                    error_msg = 'Email address cannot be blank.'
                self.cascaded_errors.append(error_msg)
        # raise all the cascaded errors now
        if len(self.cascaded_errors) > 0:
            raise forms.ValidationError(self.cascaded_errors)
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        self.email = email
        return email

    def save(self, request):
        email = self.email
        request.session[SOCIAL_REGISTRATION_SETTING_EMAIL] = email
        return email


class SocialRegistrationAuthenticationForm(UsernameEmailAuthenticationForm):
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'placeholder': 'Password', }))

    def __init__(self, email, *args, **kwargs):
        super(SocialRegistrationAuthenticationForm, self).__init__(None, *args, **kwargs)
        del self.fields['username_email']
        self.email = email

    def clean(self):
        email = self.email
        password = self.cleaned_data.get('password')
        cleaned_data = super(SocialRegistrationAuthenticationForm, self).clean(username_email=email, password=password)
        return cleaned_data


class SocialRegistrationTermsAgreementForm(forms.Form):
    agreed_to_terms = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super(SocialRegistrationTermsAgreementForm, self).__init__(*args, **kwargs)
        self.cascaded_errors = []

    def clean(self):
        cleaned_data = self.cleaned_data
        for field_name in self.fields:
            if field_name in self._errors:
                errors = self._errors[field_name]
                error_msg = errors[0]
                if error_msg == 'This field is required.':
                    error_msg = "Please check the box indicating that you agree with %s's Privacy Policy and Terms of Service." % htk_setting('HTK_SITE_NAME')  # noqa
                self.cascaded_errors.append(error_msg)
        # raise all the cascaded errors now
        if len(self.cascaded_errors) > 0:
            raise forms.ValidationError(self.cascaded_errors)
        return cleaned_data

    def save(self, request):
        agreed_to_terms = self.cleaned_data['agreed_to_terms']
        request.session[SOCIAL_REGISTRATION_SETTING_AGREED_TO_TERMS] = agreed_to_terms
        return agreed_to_terms
