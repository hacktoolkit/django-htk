# Python Standard Library Imports
import collections
import hashlib
from typing import (
    Any,
    Dict,
)

# Django Imports
from django.conf import settings
from django.db import models

# HTK Imports
from htk.apps.organizations.enums import (
    OrganizationMemberRoles,
    OrganizationTeamMemberRoles,
)
from htk.apps.organizations.utils import (
    get_model_organization_member,
    get_organization_member_role_choices,
    get_organization_team_member_role_choices,
)
from htk.models import (
    AbstractAttribute,
    AbstractAttributeHolderClassFactory,
    HtkBaseModel,
)
from htk.utils import htk_setting


# isort: off


class OrganizationAttribute(AbstractAttribute):
    holder = models.ForeignKey(htk_setting('HTK_ORGANIZATION_MODEL'), on_delete=models.CASCADE, related_name='attributes')

    class Meta:
        abstract = True
        # app_label = 'organizations'
        # verbose_name = 'Organization Attribute'
        # unique_together = (
        #     ('holder', 'key',),
        # )

    def __str__(self):
        value = '%s (%s)' % (self.key, self.holder)
        return value


OrganizationAttributeHolder = AbstractAttributeHolderClassFactory(
    OrganizationAttribute,
    holder_resolver=lambda self: self
).get_class()


class BaseAbstractOrganization(HtkBaseModel):
    name = models.CharField(max_length=128)
    handle = models.CharField(max_length=64, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
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

        if not hasattr(collections, 'MutableSet'):
            # Python >= 3.6
            # See:
            # - https://stackoverflow.com/a/53657523/865091
            # - https://stackoverflow.com/a/39980744/865091
            users = list(dict.fromkeys([member.user for member in members]))
        else:
            from htk.extensions.data_structures import OrderedSet
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

    def add_member(self, user, role):
        OrganizationMember = get_model_organization_member()
        new_member = OrganizationMember.objects.create(
            user=user,
            organization=self,
            role=role.value,
            active=True
        )
        return new_member

    def add_owner(self, user):
        OrganizationMember = get_model_organization_member()
        new_owner = self.add_member(user, OrganizationMemberRoles.OWNER)
        return new_owner


class BaseAbstractOrganizationMember(HtkBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organizations')
    organization = models.ForeignKey(htk_setting('HTK_ORGANIZATION_MODEL'), on_delete=models.CASCADE, related_name='members')
    role = models.PositiveIntegerField(default=OrganizationMemberRoles.MEMBER.value, choices=get_organization_member_role_choices())
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        verbose_name = 'Organization Member'

    def json_encode(self) -> Dict[str, Any]:
        """Returns a dictionary that can be `json.dumps()`-ed as a JSON representation of this object
        """
        value = {
            'id': self.id,
            'user': self.user.profile.get_full_name(),
            'organization': self.organization.name,
            'role': self.role,
            'active': self.active,
        }
        return value


class BaseAbstractOrganizationInvitation(HtkBaseModel):
    organization = models.ForeignKey(htk_setting('HTK_ORGANIZATION_MODEL'), on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organization_invitations_sent')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organization_invitations', blank=True, null=True, default=None)
    email = models.EmailField(blank=True, null=True, default=None) # email where invitation was originally sent
    token = models.CharField(max_length=40, unique=True)
    accepted = models.BooleanField(default=None, null=True) # True: accepted, False: declined, None: not responded yet
    timestamp = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        abstract = True
        verbose_name = 'Organization Invitation'

    def json_encode(self) -> Dict[str, Any]:
        """Returns a dictionary that can be `json.dumps()`-ed as a JSON representation of this object
        """
        value = {
            'id': self.id,
            'organization': self.organization.name,
            'invited_by': self.invited_by.profile.get_full_name(),
            'user': self.user.profile.get_full_name() if self.user else None,
            'email': self.email,
            'accepted': self.accepted,
            'invited_at': self.timestamp,
            'responded_at': self.responded_at,
        }
        return value

    ##
    # properties

    @property
    def status(self) -> str:
        status = (
            'Invited' if self.accepted is None
            else 'Accepted' if self.accepted
            else 'Declined'
        )

        return status

    ##
    # Methods

    def generate_token(self) -> None:
        """ Generates invitation token to send to the user.
        """
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
        self.token = hashlib.sha1(str(f'{salt}{self.email}').encode('utf-8')).hexdigest()

    def save(self, *args, **kwargs):
        """Overrides save method to auto-generate token for invitation.
        """
        if self.token is None:
            self.generate_token()
        else:
            pass

        super(BaseAbstractOrganizationInvitation, self).save(*args, **kwargs)


class BaseAbstractOrganizationTeam(HtkBaseModel):
    name = models.CharField(max_length=128)
    organization = models.ForeignKey(htk_setting('HTK_ORGANIZATION_MODEL'), on_delete=models.CASCADE, related_name='teams')

    class Meta:
        abstract = True
        verbose_name = 'Organization Team'

    def __str__(self):
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organization_teams')
    team = models.ForeignKey(htk_setting('HTK_ORGANIZATION_TEAM_MODEL'), on_delete=models.CASCADE, related_name='members')
    role = models.PositiveIntegerField(default=OrganizationTeamMemberRoles.MEMBER.value, choices=get_organization_team_member_role_choices())

    class Meta:
        abstract = True
        unique_together = ('user', 'team',)
        verbose_name = 'Organization Team Member'

    def __str__(self):
        value = '%s - %s' % (self.user, self.team.__str__(),)
        return value


class BaseAbstractOrganizationTeamPosition(HtkBaseModel):
    name = models.CharField(max_length=128)
    team = models.ForeignKey(htk_setting('HTK_ORGANIZATION_TEAM_MODEL'), on_delete=models.CASCADE, related_name='positions')

    class Meta:
        abstract = True
        unique_together = ('name', 'team',)
        verbose_name = 'Organization Team Position'

    def __str__(self):
        value = '%s - %s' % (self.name, self.team.__str__(),)
        return value


class BaseAbstractOrganizationTeamMemberPosition(HtkBaseModel):
    member = models.ForeignKey(htk_setting('HTK_ORGANIZATION_TEAM_MEMBER_MODEL'), on_delete=models.CASCADE, related_name='positions')
    position = models.ForeignKey(htk_setting('HTK_ORGANIZATION_TEAM_POSITION_MODEL'), on_delete=models.CASCADE, related_name='team_members')

    class Meta:
        abstract = True
        verbose_name = 'Organization Team Member Position'

    def __str__(self):
        value = '%s - %s' % (self.position.name, self.member.__str__(),)
        return value
