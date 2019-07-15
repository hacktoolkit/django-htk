# Python Standard Library Imports

# Third Party / PIP Imports

# Django Imports
from django.conf import settings
from django.db import models

# HTK Imports
from htk.apps.organizations.enums import OrganizationMemberRoles
from htk.apps.organizations.enums import OrganizationTeamMemberRoles
from htk.apps.organizations.utils import get_organization_member_role_choices
from htk.apps.organizations.utils import get_organization_team_member_role_choices
from htk.models import AbstractAttribute
from htk.models import AbstractAttributeHolderClassFactory
from htk.models import HtkBaseModel
from htk.utils import htk_setting
from htk.extensions.data_structures import OrderedSet

class OrganizationAttribute(AbstractAttribute):
    holder = models.ForeignKey(htk_setting('HTK_ORGANIZATION_MODEL'), related_name='attributes')

    class Meta:
        app_label = 'organizations'
        verbose_name = 'Organization Attribute'
        unique_together = (
            ('holder', 'key',),
        )

    def __unicode__(self):
        value = '%s (%s)' % (self.key, self.holder)
        return value


OrganizationAttributeHolder = AbstractAttributeHolderClassFactory(
    OrganizationAttribute,
    holder_resolver=lambda self: self
).get_class()


class BaseAbstractOrganization(HtkBaseModel, OrganizationAttributeHolder):
    name = models.CharField(max_length=128)
    handle = models.CharField(max_length=64, unique=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        value = '%s' % (self.name,)
        return value

    def json_encode(self):
        """Returns a dictionary that can be `json.dumps()`-ed as a JSON representation of this object
        """
        value = super(BaseAbstractOrganization, self).json_encode()
        value.update({
            'name' : self.name,
            'handle' : self.handle,
        })
        return value

    ##
    # Accessors

    def get_members(self):
        sort_order = htk_setting('HTK_ORGANIZATION_MEMBERS_SORT_ORDER')
        members = self.members.filter(
            active=True,
            user__is_active=True
        ).order_by(
            *sort_order
        )
        return members

    def get_distinct_members(self):
        members = self.get_members()
        users_set = OrderedSet([member.user for member in members])
        users = list(users_set)
        return users

    ##
    # ACLs

    def _has_member_with_role(self, user, roles):
        role_values = [role.value for role in roles]
        has_member = self.members.filter(user=user, role__in=role_values)
        return has_member

    def has_owner(self, user):
        roles = (
            OrganizationMemberRoles.OWNER,
        )
        return self._has_member_with_role(user, roles=roles)

    def has_admin(self, user):
        roles = (
            OrganizationMemberRoles.OWNER,
            OrganizationMemberRoles.ADMIN,
        )
        return self._has_member_with_role(user, roles=roles)

    def has_member(self, user):
        roles = (
            OrganizationMemberRoles.OWNER,
            OrganizationMemberRoles.ADMIN,
            OrganizationMemberRoles.MEMBER,
        )
        return self._has_member_with_role(user, roles=roles)


class BaseAbstractOrganizationMember(HtkBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='organizations')
    organization = models.ForeignKey(htk_setting('HTK_ORGANIZATION_MODEL'), related_name='members')
    role = models.PositiveIntegerField(default=OrganizationMemberRoles.MEMBER.value, choices=get_organization_member_role_choices())
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        verbose_name = 'Organization Member'


class BaseAbstractOrganizationInvitation(HtkBaseModel):
    organization = models.ForeignKey(htk_setting('HTK_ORGANIZATION_MODEL'), related_name='invitations')
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='organization_invitations_sent')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='organization_invitations', blank=True, null=True, default=None)
    email = models.EmailField(blank=True, null=True, default=None) # email where invitation was originally sent
    accepted = models.NullBooleanField(default=None) # True: accepted, False: declined, None: not responded yet
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        verbose_name = 'Organization Invitation'


class BaseAbstractOrganizationTeam(HtkBaseModel):
    name = models.CharField(max_length=128)
    organization = models.ForeignKey(htk_setting('HTK_ORGANIZATION_MODEL'), related_name='teams')

    class Meta:
        abstract = True
        verbose_name = 'Organization Team'

    def __unicode__(self):
        value = '%s (%s)' % (self.name, self.organization.name,)
        return value

    ##
    # Accessors

    def get_members(self):
        sort_order = htk_setting('HTK_ORGANIZATION_TEAM_MEMBERS_SORT_ORDER')
        members = self.members.filter(
            #active=True, # TODO: exclude users that are not active at the organization level
            user__is_active=True
        ).order_by(
            *sort_order
        )
        return members


class BaseAbstractOrganizationTeamMember(HtkBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='organization_teams')
    team = models.ForeignKey(htk_setting('HTK_ORGANIZATION_TEAM_MODEL'), related_name='members')
    role = models.PositiveIntegerField(default=OrganizationTeamMemberRoles.MEMBER.value, choices=get_organization_team_member_role_choices())

    class Meta:
        abstract = True
        unique_together = ('user', 'team',)
        verbose_name = 'Organization Team Member'

    def __unicode__(self):
        value = '%s - %s' % (self.user, self.team.__unicode__(),)
        return value


class BaseAbstractOrganizationTeamPosition(HtkBaseModel):
    name = models.CharField(max_length=128)
    team = models.ForeignKey(htk_setting('HTK_ORGANIZATION_TEAM_MODEL'), related_name='positions')

    class Meta:
        abstract = True
        unique_together = ('name', 'team',)
        verbose_name = 'Organization Team Position'

    def __unicode__(self):
        value = '%s - %s' % (self.name, self.team.__unicode__(),)
        return value


class BaseAbstractOrganizationTeamMemberPosition(HtkBaseModel):
    member = models.ForeignKey(htk_setting('HTK_ORGANIZATION_TEAM_MEMBER_MODEL'), related_name='positions')
    position = models.ForeignKey(htk_setting('HTK_ORGANIZATION_TEAM_POSITION_MODEL'), related_name='team_members')

    class Meta:
        abstract = True
        verbose_name = 'Organization Team Member Position'

    def __unicode__(self):
        value = '%s - %s' % (self.position.name, self.member.__unicode__(),)
        return value
