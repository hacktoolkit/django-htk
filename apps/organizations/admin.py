# Python Standard Library Imports

# Third Party / PIP Imports

# Django Imports
from django.contrib import admin

# HTK Imports
from htk.apps.organizations.models import OrganizationAttribute
from htk.utils import htk_setting
from htk.utils.general import resolve_model_dynamically


class HtkOrganizationAttributeInline(admin.TabularInline):
    model = OrganizationAttribute
    extra = 0
    can_delete = True


class HtkOrganizationMemberInline(admin.TabularInline):
    model = resolve_model_dynamically(htk_setting('HTK_ORGANIZATION_MEMBER_MODEL'))
    extra = 0
    can_delete = True


class HtkOrganizationInvitationInline(admin.TabularInline):
    model = resolve_model_dynamically(htk_setting('HTK_ORGANIZATION_INVITATION_MODEL'))
    extra = 0
    can_delete = True


class HtkOrganizationTeamMemberInline(admin.TabularInline):
    model = resolve_model_dynamically(htk_setting('HTK_ORGANIZATION_TEAM_MEMBER_MODEL'))
    extra = 0
    can_delete = True


class HtkOrganizationTeamMemberPositionInline(admin.TabularInline):
    model = resolve_model_dynamically(htk_setting('HTK_ORGANIZATION_TEAM_MEMBER_POSITION_MODEL'))
    extra = 0
    can_delete = True


class HtkOrganizationTeamInline(admin.StackedInline):
    model = resolve_model_dynamically(htk_setting('HTK_ORGANIZATION_TEAM_MODEL'))
    extra = 0
    can_delete = True


class HtkOrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'handle',
    )
    inlines = (
        HtkOrganizationAttributeInline,
        HtkOrganizationMemberInline,
        HtkOrganizationTeamInline,
        HtkOrganizationInvitationInline,
    )


class HtkOrganizationMemberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'organization',
        'role',
    )


class HtkOrganizationTeamAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'organization',
    )
    inlines = (
        HtkOrganizationTeamMemberInline,
    )

class HtkOrganizationTeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'team',
        'role',
    )
    inlines = (
        HtkOrganizationTeamMemberPositionInline,
    )


class HtkOrganizationTeamPositionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'team',
        'name',
    )


class OrganizationMemberInline(admin.TabularInline):
    model = 'organizations.OrganizationMember'
