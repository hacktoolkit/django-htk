from django import forms
from htk.apps.accounts.utils.general import get_user_by_id


class HTKOrganizationTeamForm(forms.ModelForm):
    ERROR_MESSAGES = {
        'already_member': 'A team with this name already exists',
    }

    class Meta:
        fields = ['name']

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


class HTKOrganizationTeamMemberForm(forms.ModelForm):
    ERROR_MESSAGES = {
        'user_not_found': 'There is no user with this email address',
        'already_member': 'That user is already a member of this team.',
    }

    user_id = forms.CharField(max_length=5)

    class Meta:
        fields = ['user_id']

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
