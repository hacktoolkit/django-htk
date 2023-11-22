# Django Imports
from django import forms

# HTK Imports
from htk.apps.accounts.utils import get_user_by_id, get_user_by_email
from htk.apps.organizations.utils import invite_organization_member


class AbstractOrganizationInvitationForm(forms.ModelForm):
    ERROR_MESSAGES = {
        'already_accepted': 'This email address has already been accepted the invitation.',
    }

    class Meta:
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def __init_subclass__(cls, model, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.Meta.model = model

    def __init__(self, organization, invited_by, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.organization = organization
        self.instance.invited_by = invited_by

    def clean_email(self):
        email = self.cleaned_data.get('email')

        q = self.instance.organization.invitations.filter(email=email)
        if q.exists():
            self.instance = q.first()
        else:
            pass

        if self.instance.accepted:
            raise forms.ValidationError(self.ERROR_MESSAGES['already_accepted'])
        else:
            pass

        return email

    def save(self, request, *args, **kwargs):
        invitation = super().save(commit=False)
        invitation = invite_organization_member(request, invitation)
        return invitation


class AbstractOrganizationMemberForm(forms.ModelForm):
    ERROR_MESSAGES = {
        'user_not_found': 'There is no user with this email address',
        'already_member': 'That user is already a member of this organization.',
    }

    class Meta:
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def __init_subclass__(cls, model, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.Meta.model = model

    def __init__(self, organization, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.organization = organization

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = get_user_by_email(email)

        if user is None:
            raise forms.ValidationError(self.ERROR_MESSAGES['user_not_found'])
        else:
            pass

        q = self.instance.organization.members.filter(user__id=user.id)
        if q.exists():
            raise forms.ValidationError(self.ERROR_MESSAGES['already_member'])
        else:
            pass

        return email


class AbstractOrganizationTeamForm(forms.ModelForm):
    ERROR_MESSAGES = {
        'already_member': 'A team with this name already exists',
    }

    class Meta:
        fields = ['name']

    def __init_subclass__(cls, model, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.Meta.model = model

    def __init__(self, organization, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.organization = organization

    def clean_name(self):
        team_name = self.cleaned_data.get('name')
        q = self.instance.organization.teams.filter(name=team_name)
        # NOTE: If this form is being used to edit a team, we should exclude the
        # current team from filter.
        if self.instance.id is not None:
            q = q.exclude(id=self.instance.id)
        if q.exists():
            raise forms.ValidationError(self.ERROR_MESSAGES['already_member'])

        return team_name


class AbstractOrganizationTeamMemberForm(forms.ModelForm):
    ERROR_MESSAGES = {
        'user_not_found': 'There is no user with this email address',
        'already_member': 'That user is already a member of this team.',
    }

    user_id = forms.CharField(max_length=5)

    class Meta:
        fields = ['user_id']

    def __init_subclass__(cls, model, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.Meta.model = model

    def __init__(self, team, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.team = team

    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id')
        user = get_user_by_id(user_id)
        if user is None:
            raise forms.ValidationError(self.ERROR_MESSAGES['user_not_found'])
        else:
            pass

        q = self.instance.team.members.filter(user__id=user.id).first()
        if q is not None:
            raise forms.ValidationError(self.ERROR_MESSAGES['already_member'])
        else:
            pass

        self.instance.user = user
        return user
