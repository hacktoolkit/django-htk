# Django Imports
from django.http import Http404
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

# HTK Imports
from htk.apps.organizations.enums import OrganizationMemberRoles
from htk.utils import htk_setting
from htk.utils.general import resolve_model_dynamically


class require_organization_permission(object):
    """Decorator for requiring current logged-in user to have required level of permission in Organization
    """
    def __init__(self, role):
        self.role = role

    def __call__(self, view_func):
        def wrapped_view(request, *args, **kwargs):
            organization_id = kwargs.get('org_id')
            Organization = resolve_model_dynamically(htk_setting('HTK_ORGANIZATION_MODEL'))
            organization = get_object_or_404(Organization, id=organization_id)
            kwargs['organization'] = organization

            has_permission = False
            user = request.user
            if user.is_authenticated:
                if self.role == OrganizationMemberRoles.OWNER:
                    has_permission = organization.has_owner(user)
                elif self.role == OrganizationMemberRoles.ADMIN:
                    has_permission = organization.has_admin(user)
                elif self.role == OrganizationMemberRoles.MEMBER:
                    has_permission = organization.has_member(user)

            if has_permission:
                response = view_func(request, *args, **kwargs)
            else:
                response = HttpResponseForbidden()
            return response
        return wrapped_view

def require_organization_owner(view_func):
    return require_organization_permission(OrganizationMemberRoles.OWNER)(view_func)

def require_organization_admin(view_func):
    return require_organization_permission(OrganizationMemberRoles.ADMIN)(view_func)

def require_organization_member(view_func):
    return require_organization_permission(OrganizationMemberRoles.MEMBER)(view_func)
