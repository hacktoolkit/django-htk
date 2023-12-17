# Python Standard Library Imports
import json

# Django Imports
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

# HTK Imports
from htk.api.utils import (
    json_response_error,
    json_response_form_error,
    json_response_okay,
)
from htk.apps.organizations.decorators import (
    require_organization_admin,
    require_organization_member,
    require_organization_member_user,
    require_organization_team,
    require_organization_invitation,
)
from htk.apps.organizations.enums import OrganizationMemberRoles
from htk.utils import (
    htk_setting,
    resolve_method_dynamically,
    resolve_model_dynamically,
)
from htk.view_helpers import render_custom as _r


class BaseFormRequiredView(View):
    """Base Form Required View

    TODO: Move this to htk.view_helpers when approved.
    """

    FORM = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.FORM is None:
            raise NotImplementedError(
                f'{self.__class__.__name__} must define FORM'
            )


class OrganizationInvitationResponseView(View):
    """Organization Invitation Response Class Based View

    This class view intended to be extended in project to set the custom render
    method and template name there.

    Template should contain a form with POST method and should send `response`
    variable to this view's POST method.

    `response` value should be either `accept` or `decline`.

    Sample template form:
    ```
    <form action="" method="post">
    <button type="submit" name="response" value="accept">Accept</button>
    <button type="submit" name="response" value="decline">Decline</button>
    </form>
    ```
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_method = _r
        self.template_name = 'organizations/invitation_response.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        token = kwargs.pop('token')
        OrganizationInvitation = resolve_model_dynamically(
            htk_setting('HTK_ORGANIZATION_INVITATION_MODEL')
        )
        invitation = get_object_or_404(OrganizationInvitation, token=token)
        user = request.user if request.user.is_authenticated else None

        # Logged in user cannot accept invitation in place of someone else.
        if (
            user
            and user.email != invitation.email
            and not (user.profile.has_email(invitation.email))
        ):
            raise Http404

        # Set variables that might be needed
        self.invitation = invitation
        self.model = OrganizationInvitation

        # Prepare context data for both GET and POST methods
        self.build_context()
        self.data['invitation'] = self.invitation

    def get(self, request, *args, **kwargs):
        response = self.render_method(request, self.template_name, self.data)
        return response

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        invitation_response = request.POST.get('response', None)

        self.invitation.accepted = invitation_response == 'accept'
        self.invitation.responded_at = timezone.datetime.now()

        self.invitation.user = request.user
        if self.invitation.accepted:
            # TODO: adding as member but maybe this should be a setting?
            self.invitation.organization.add_member(
                self.invitation.user, OrganizationMemberRoles.MEMBER
            )

        self.invitation.save()

        self.data['invitation_accepted'] = self.invitation.accepted

        response = self.render_method(request, self.template_name, self.data)
        return response

    def build_context(self):
        wrap_data = resolve_method_dynamically(
            htk_setting('HTK_VIEW_CONTEXT_GENERATOR')
        )
        self.data = wrap_data(self.request)


@method_decorator(
    require_organization_admin(content_type='application/json'), name='dispatch'
)
class OrganizationInvitationsAPIView(BaseFormRequiredView):
    """Organization Invitations API Endpoint

    NOTE: `FORM` must be defined in the subclass
    """

    ORDER_BY = ['-responded_at']

    def get(self, request, *args, **kwargs):
        organization = kwargs.pop('organization')
        invitations = organization.invitations.order_by(*self.ORDER_BY)
        response = json_response_okay(
            {
                'object': 'list',
                'data': [
                    invitation.json_encode() for invitation in invitations
                ],
            }
        )
        return response

    def post(self, request, *args, **kwargs):
        organization = kwargs.pop('organization')
        data = json.loads(request.body)
        user = request.user

        form = self.FORM(organization, user, data)

        if form.is_valid():
            invitation = form.save(request)
            response = json_response_okay(invitation.json_encode())
        else:
            response = json_response_form_error(form)

        return response


@method_decorator(
    require_organization_admin(content_type='application/json'), name='dispatch'
)
@method_decorator(
    require_organization_invitation(content_type='application/json'),
    name='dispatch',
)
class OrganizationInvitationAPIView(View):
    def delete(self, request, *args, **kwargs):
        invitation = kwargs.pop('invitation')

        invitation.delete()

        response = json_response_okay()
        return response


class OrganizationMembersAPIView(BaseFormRequiredView):
    """Organization Members API Endpoint

    NOTE: `FORM` must be defined in the subclass
    """

    @method_decorator(
        require_organization_member(content_type='application/json')
    )
    def get(self, request, *args, **kwargs):
        organization = kwargs.pop('organization')
        members = organization.get_distinct_members()
        response = json_response_okay(
            {
                'object': 'list',
                'data': [member.json_encode() for member in members],
            }
        )
        return response

    @method_decorator(
        require_organization_admin(content_type='application/json')
    )
    def post(self, request, *args, **kwargs):
        organization = kwargs.pop('organization')
        data = json.loads(request.body)
        form = self.FORM(organization, data)

        if form.is_valid():
            member = form.save()
            response = json_response_okay(member.json_encode())
        else:
            response = json_response_form_error(form)

        return response


@method_decorator(
    require_organization_admin(content_type='application/json'), name='dispatch'
)
@method_decorator(
    require_organization_member_user(content_type='application/json'),
    name='dispatch',
)
class OrganizationMemberAPIView(View):
    def delete(self, request, *args, **kwargs):
        member = kwargs.pop('member')
        member.delete()
        response = json_response_okay()

        return response


class OrganizationTeamsAPIView(BaseFormRequiredView):
    """Organization Teams API Endpoint

    NOTE: `FORM` must be defined in the subclass
    """

    @method_decorator(
        require_organization_member(content_type='application/json')
    )
    def get(self, request, *args, **kwargs):
        organization = kwargs.pop('organization')
        teams = organization.teams.all()
        response = json_response_okay(
            {
                'object': 'list',
                'data': [team.json_encode() for team in teams],
            }
        )
        return response

    @method_decorator(
        require_organization_admin(content_type='application/json')
    )
    def post(self, request, *args, **kwargs):
        organization = kwargs.pop('organization')
        data = json.loads(request.body)
        form = self.FORM(organization, data)

        if form.is_valid():
            team = form.save()
            response = json_response_okay(team.json_encode())
        else:
            response = json_response_form_error(form)

        return response


@method_decorator(
    require_organization_admin(content_type='application/json'), name='dispatch'
)
@method_decorator(
    require_organization_team(content_type='application/json'), name='dispatch'
)
class OrganizationTeamAPIView(BaseFormRequiredView):
    """Organization Team API Endpoint

    NOTE: `FORM` must be defined in the subclass
    """

    MESSAGES = {
        'delete_failed': 'This team can not be deleted until all other members have been removed.',
    }

    def patch(self, request, *args, **kwargs):
        """Update existing Organization Team"""
        organization = kwargs.pop('organization')
        team = kwargs.pop('team')
        data = json.loads(request.body)
        form = self.FORM(organization, data, instance=team)

        if form.is_valid():
            team = form.save()
            response = json_response_okay(team.json_encode())
        else:
            response = json_response_form_error(form)

        return response

    def delete(self, request, *args, **kwargs):
        """Delete existing Organization Team"""
        team = kwargs.pop('team')
        was_deleted = team.delete()
        if was_deleted:
            response = json_response_okay()
        else:
            response = json_response_error(
                {'error': self.MESSAGES['delete_failed']}
            )

        return response


class OrganizationTeamMembersAPIView(BaseFormRequiredView):
    """Organization Team Members API Endpoint

    NOTE: `FORM` must be defined in the subclass
    """

    @method_decorator(
        require_organization_member(content_type='application/json')
    )
    @method_decorator(
        require_organization_team(content_type='application/json')
    )
    def get(self, request, *args, **kwargs):
        team = kwargs.pop('team')
        team_members = team.get_members()
        response = json_response_okay(
            {
                'object': 'list',
                'data': [
                    team_member.json_encode() for team_member in team_members
                ],
            }
        )

        return response

    @method_decorator(
        require_organization_admin(content_type='application/json')
    )
    @method_decorator(
        require_organization_team(content_type='application/json')
    )
    def post(self, request, *args, **kwargs):
        """Add existing user as new Organization Team Member"""
        team = kwargs.pop('team')
        data = json.loads(request.body)
        form = self.FORM(team, data)

        if form.is_valid():
            team_member = form.save()
            response = json_response_okay(team_member.json_encode())
        else:
            response = json_response_form_error(form)

        return response


@method_decorator(
    require_organization_admin(content_type='application/json'), name='dispatch'
)
@method_decorator(
    require_organization_team(content_type='application/json'), name='dispatch'
)
class OrganizationTeamMemberAPIView(View):
    def delete(self, request, member_id, *args, **kwargs):
        """Delete existing Organization Team Member"""
        team = kwargs.pop('team')
        user = request.user

        (deleted_count, _) = (
            team.members.exclude(user=user).filter(user__id=member_id).delete()
        )

        if deleted_count == 0:
            response = json_response_error(
                {'message': 'This member can not be deleted.'}
            )
        else:
            response = json_response_okay()

        return response
