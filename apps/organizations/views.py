# Django Imports
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

# HTK Imports
from htk.utils import (
    htk_setting,
    resolve_method_dynamically,
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
        self.build_context()
        self.data['invitation'] = self.invitation

    def get(self, request, *args, **kwargs):
        is_mobile = request.user_agent.is_mobile or request.user_agent.is_tablet
        mobile_invitation_response_url_format = htk_setting(
            'HTK_ORGANIZATION_MOBILE_INVITATION_RESPONSE_URL_FORMAT'
        )
        if is_mobile and mobile_invitation_response_url_format:
            token = self.invitation.token
            self.data['mobile_invitation_response_url'] = (
                mobile_invitation_response_url_format.format(
                    token_hex=token.hex
                )
            )
            self.data['appstore_url'] = htk_setting('HTK_APPSTORE_URL')
        else:
            # Is not on mobile, render on the web
            pass

        response = self.render_method(request, self.template_name, self.data)
        return response

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        invitation_response = request.POST.get('response', None)
        if invitation_response == 'accept':
            self.invitation.accept()
        else:
            self.invitation.decline()

        self.data['invitation_accepted'] = self.invitation.accepted

        response = self.render_method(request, self.template_name, self.data)
        return response

    def build_context(self):
        wrap_data = resolve_method_dynamically(
            htk_setting('HTK_VIEW_CONTEXT_GENERATOR')
        )
        self.data = wrap_data(self.request)
