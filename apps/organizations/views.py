# Django Imports
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

# HTK Imports
from htk.apps.organizations.enums import OrganizationMemberRoles
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)
from htk.view_helpers import render_custom as _r


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
        if self.data and type(self.data) == 'dict':
            self.data.update(
                {
                    'invitation': self.invitation,
                }
            )
        else:
            self.data = {'invitation': self.invitation}

    def get(self, request, *args, **kwargs):
        response = self.render_method(request, self.template_name, self.data)
        return response

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        invitation_response = request.POST.get('response', None)

        self.invitation.accepted == invitation_response == 'accept'
        self.invitation.responded_at = timezone.datetime.now()

        if self.invitation.accepted:
            self.invitation.user = request.user
            # TODO: adding as member but maybe this should be a setting?
            self.invitation.organization.add_member(
                self.invitation.user, OrganizationMemberRoles.MEMBER
            )

        self.invitation.save()

        self.data['invitation_accepted'] = self.invitation.accepted

        response = self.render_method(request, self.template_name, self.data)
        return response
