# Python Standard Library Imports
from functools import wraps

# Django Imports
from django.http import (
    Http404,
    HttpResponseForbidden,
)
from django.shortcuts import get_object_or_404

# HTK Imports
from htk.api.utils import json_response_error
from htk.apps.organizations.enums import OrganizationMemberRoles
from htk.utils import htk_setting
from htk.utils.general import resolve_model_dynamically


class require_organization_permission(object):
    """Decorator for requiring current logged-in user to have required level of permission in Organization."""

    def __init__(self, role, content_type='text/html'):
        self.role = role
        self.content_type = content_type

    def __call__(self, view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            response = None

            org_url_pk_key = htk_setting('HTK_ORGANIZATION_URL_PK_KEY')
            organization_id = kwargs.get(org_url_pk_key)
            handle = kwargs.get('handle')

            if organization_id is None and handle is None:
                raise Exception(
                    'One of {org_url_pk_key} or handle must be specified'.format(
                        org_url_pk_key=org_url_pk_key
                    )
                )

            key = 'id' if organization_id else 'handle'
            pk = organization_id if organization_id else handle
            Organization = resolve_model_dynamically(
                htk_setting('HTK_ORGANIZATION_MODEL')
            )

            try:
                organization = Organization.objects.get(**{key: pk})
            except Organization.DoesNotExist:
                if self.content_type == 'application/json':
                    response = json_response_error(
                        {
                            'error': '{readable_name} not found'.format(
                                readable_name=htk_setting(
                                    'HTK_ORGANIZATION_READABLE_NAME'
                                )
                            )
                        },
                        status=404,
                    )
                else:
                    raise Http404

            if response is None:
                kwargs[htk_setting('HTK_ORGANIZATION_SYMBOL')] = organization

            user = request.user
            has_permission = user.is_authenticated and (
                (
                    self.role == OrganizationMemberRoles.OWNER
                    and organization.has_owner(user)
                )
                or (
                    self.role == OrganizationMemberRoles.ADMIN
                    and organization.has_admin(user)
                )
                or (
                    self.role == OrganizationMemberRoles.MEMBER
                    and organization.has_member(user)
                )
            )

            if has_permission:
                response = view_func(request, *args, **kwargs)
            else:
                response = (
                    json_response_error({'error': 'Forbidden'}, status=403)
                    if self.content_type == 'application/json'
                    else HttpResponseForbidden()
                )

            return response

        return wrapped_view


class require_organization_owner(object):
    def __init__(self, content_type='text/html'):
        self.content_type = content_type

    def __call__(self, view_func):
        return require_organization_permission(
            OrganizationMemberRoles.OWNER, content_type=self.content_type
        )(view_func)


class require_organization_admin(object):
    def __init__(self, content_type='text/html'):
        self.content_type = content_type

    def __call__(self, view_func):
        return require_organization_permission(
            OrganizationMemberRoles.ADMIN, content_type=self.content_type
        )(view_func)


class require_organization_member(object):
    def __init__(self, content_type='text/html'):
        self.content_type = content_type

    def __call__(self, view_func):
        return require_organization_permission(
            OrganizationMemberRoles.MEMBER, content_type=self.content_type
        )(view_func)
