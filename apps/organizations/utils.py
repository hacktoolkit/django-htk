# Django Imports
from django.apps import apps
from django.contrib.sites.shortcuts import get_current_site

# HTK Imports
from htk.apps.organizations.emailers import send_invitation_email
from htk.apps.prelaunch.utils import is_prelaunch_mode
from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically
from htk.utils.enums import get_enum_symbolic_name


# isort: off


def get_model_organization_member():
    OrganizationMember = resolve_model_dynamically(htk_setting('HTK_ORGANIZATION_MEMBER_MODEL'))
    return OrganizationMember


def get_organization_member_role_choices():
    from htk.apps.organizations.enums import OrganizationMemberRoles
    choices = [(role.value, get_enum_symbolic_name(role),) for role in OrganizationMemberRoles]
    return choices


def get_organization_team_member_role_choices():
    from htk.apps.organizations.enums import OrganizationTeamMemberRoles
    choices = [(role.value, get_enum_symbolic_name(role),) for role in OrganizationTeamMemberRoles]
    return choices


def get_user_organizations_with_attribute(user, key):
    organizations = user.organizations.filter(
        active=True,
        organization__attributes__key=key
    ).exclude(
        organization__attributes__value=None
    )
    return organizations


def invite_organization_member(request, invitation):
    """Invite person to organization

    Sends invitation e-mail to given person.
    If prelaunch app is installed, in prelaunch mode and auto adding to waiting list enabled,
    it adds early access code to invitation link.
    This function can also be used for re-send invitation links.

    Args:
        request (Request): Request object. It is needed to build full URL and get current site
        invitation (BaseAbstractOrganizationInvitation): Invitation object can be come from form.
    """
    early_access_code = None
    if (
        apps.is_installed('htk.apps.prelaunch')
        and is_prelaunch_mode()
        and htk_setting('HTK_ORGANIZATION_INVITATION_AUTO_ADD_TO_WAIT_LIST')
    ):
        from htk.apps.prelaunch.utils import PrelaunchSignup
        prelaunch_signup = (
            PrelaunchSignup.get_or_create_by_email(
                email=invitation.email,
                first_name=invitation.first_name,
                last_name=invitation.last_name,
                site=get_current_site(request),
                enable_early_access=True,
            )
        )
        early_access_code = prelaunch_signup.early_access_code
    else:
        pass

    if invitation.accepted is not None:
        # If invitation is not Invited status, update to Invited.
        invitation.accepted = None
    else:
        pass

    # Save invitation so that updatedAt field will be updated
    invitation.save()

    send_invitation_email(
        request, invitation, early_access_code=early_access_code
    )
