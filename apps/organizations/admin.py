# Django Imports
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

# HTK Imports
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)


class HtkOrganizationAttributeInline(admin.TabularInline):
    model = resolve_model_dynamically(
        htk_setting('HTK_ORGANIZATION_ATTRIBUTE_MODEL')
    )
    extra = 0
    can_delete = True


class HtkOrganizationMemberInline(admin.TabularInline):
    model = resolve_model_dynamically(
        htk_setting('HTK_ORGANIZATION_MEMBER_MODEL')
    )
    extra = 0
    can_delete = True


class HtkOrganizationInvitationInline(admin.TabularInline):
    model = resolve_model_dynamically(
        htk_setting('HTK_ORGANIZATION_INVITATION_MODEL')
    )
    extra = 0
    can_delete = True


class HtkOrganizationTeamMemberInline(admin.TabularInline):
    model = resolve_model_dynamically(
        htk_setting('HTK_ORGANIZATION_TEAM_MEMBER_MODEL')
    )
    extra = 0
    can_delete = True


class HtkOrganizationTeamMemberPositionInline(admin.TabularInline):
    model = resolve_model_dynamically(
        htk_setting('HTK_ORGANIZATION_TEAM_MEMBER_POSITION_MODEL')
    )
    extra = 0
    can_delete = True


class HtkOrganizationTeamInline(admin.StackedInline):
    model = resolve_model_dynamically(
        htk_setting('HTK_ORGANIZATION_TEAM_MODEL')
    )
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
        # HtkOrganizationMemberInline,
        # HtkOrganizationTeamInline,
        # HtkOrganizationInvitationInline,
    )


class HtkOrganizationMemberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        # 'organization',
        'organization_filter',
        'user',
        'role',
    )

    list_filter = (
        'organization',
        'role',
    )
    search_fields = (
        'organization',
        'user',
    )

    @mark_safe
    def organization_filter(self, obj):
        url = '{}?organization__id__exact={}'.format(
            reverse('admin:organizations_organizationmember_changelist'),
            obj.organization.id,
        )
        value = f'<a href="{url}">{obj.organization.name}</a>'
        return value


class HtkOrganizationInvitationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'organization',
        'invited_by',
        'user',
        'email',
        'token',
        'accepted',
        'timestamp',
        'responded_at',
    )


class HtkOrganizationTeamAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'organization',
    )
    inlines = (HtkOrganizationTeamMemberInline,)


class HtkOrganizationTeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'team',
        'user',
        'role',
    )
    inlines = (HtkOrganizationTeamMemberPositionInline,)


class HtkOrganizationTeamPositionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'team',
        'name',
    )
