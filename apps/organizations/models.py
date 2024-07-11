# Python Standard Library Imports
import uuid
from typing import (
    Any,
    Dict,
)

# Third Party (PyPI) Imports
from six.moves import collections_abc

# Django Imports
from django.db import models

# HTK Imports
from htk.apps.organizations.enums import (
    OrganizationMemberRoles,
    OrganizationTeamMemberRoles,
)
from htk.apps.organizations.fk_fields import fk_organization
from htk.apps.organizations.mixins import GoogleOrganizationMixin
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
from htk.models.fk_fields import fk_user
from htk.utils import htk_setting


# isort: off


class OrganizationAttribute(AbstractAttribute):
    holder = models.ForeignKey(
        htk_setting('HTK_ORGANIZATION_MODEL'),
        on_delete=models.CASCADE,
        related_name='attributes',
    )

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
    OrganizationAttribute, holder_resolver=lambda self: self
).get_class()


class BaseAbstractOrganization(HtkBaseModel, GoogleOrganizationMixin):
    name = models.CharField(max_length=128)
    handle = models.CharField(max_length=64, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        value = '%s' % (self.name,)
        return value

    def json_encode(self):
        """Returns a dictionary that can be `json.dumps()`-ed as a JSON representation of this object"""
        value = super(BaseAbstractOrganization, self).json_encode()
        value.update(
            {
                'name': self.name,
                'handle': self.handle,
            }
        )
        return value

    ##
    # URLs

    def get_full_url(self):
        return ''

    def get_logo_full_url(self):
        return ''

    ##
    # Accessors

    def get_members(self):
        sort_order = htk_setting('HTK_ORGANIZATION_MEMBERS_SORT_ORDER')
        members = self.members.filter(
            active=True, user__is_active=True
        ).order_by(*sort_order)
        return members

    def get_distinct_members(self):
        members = self.get_members()

        if not hasattr(collections_abc, 'MutableSet'):
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

    def look_up_member_with_role(self, user, roles):
        role_values = [role.value for role in roles]
        member = self.members.filter(user=user, role__in=role_values)
        return member

    def look_up_member(self, user):
        roles = (
            OrganizationMemberRoles.SYSADMIN,
            OrganizationMemberRoles.OWNER,
            OrganizationMemberRoles.ADMIN,
            OrganizationMemberRoles.MEMBER,
        )
        member = self.look_up_member_with_role(user, roles)
        return member

    def _has_member_with_role(self, user, roles):
        member = self.look_up_member_with_role(user, roles)
        has_member = member.exists()
        return has_member

    def has_sysadmin(self, user):
        roles = (OrganizationMemberRoles.SYSADMIN,)
        return self._has_member_with_role(user, roles=roles)

    def has_owner(self, user):
        roles = (
            OrganizationMemberRoles.SYSADMIN,
            OrganizationMemberRoles.OWNER,
        )
        return self._has_member_with_role(user, roles=roles)

    def has_admin(self, user):
        roles = (
            OrganizationMemberRoles.SYSADMIN,
            OrganizationMemberRoles.OWNER,
            OrganizationMemberRoles.ADMIN,
        )
        return self._has_member_with_role(user, roles=roles)

    def has_member(self, user):
        roles = (
            OrganizationMemberRoles.SYSADMIN,
            OrganizationMemberRoles.OWNER,
            OrganizationMemberRoles.ADMIN,
            OrganizationMemberRoles.MEMBER,
        )
        return self._has_member_with_role(user, roles=roles)

    def add_member(self, user, role, allow_duplicates=False):
        OrganizationMember = get_model_organization_member()
        if not self.has_member(user) or allow_duplicates:
            member = OrganizationMember.objects.create(
                user=user, organization=self, role=role.value, active=True
            )
        else:
            member = self.modify_member_role(user, role)

        return member

    def add_owner(self, user):
        OrganizationMember = get_model_organization_member()

        # Owner should be an existing member
        new_owner = (
            self.add_member(user, OrganizationMemberRoles.OWNER)
            if OrganizationMember.objects.filter(user=user)
            else None
        )
        return new_owner

    def modify_member_role(self, user, role):
        OrganizationMember = get_model_organization_member()
        existing_member = OrganizationMember.objects.filter(user=user).first()
        if existing_member is not None:
            existing_member.set_role(role, should_activate=True)


class BaseAbstractOrganizationMember(HtkBaseModel):
    organization = fk_organization(related_name='members', required=True)
    user = fk_user(related_name='organizations', required=True)
    role = models.PositiveIntegerField(
        default=OrganizationMemberRoles.MEMBER.value,
        choices=get_organization_member_role_choices(),
    )
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        verbose_name = 'Organization Member'
        unique_together = (
            'user',
            'organization',
        )

    def __str__(self):
        value = '{organization_name} Member - {member_name} ({member_email})'.format(
            organization_name=self.organization.name,
            member_name=self.user.profile.get_full_name(),
            member_email=self.user.email,
        )
        return value

    def json_encode(self) -> Dict[str, Any]:
        """Returns a dictionary that can be `json.dumps()`-ed as a JSON representation of this object"""
        value = {
            'id': self.id,
            'user': self.user.profile.get_full_name(),
            'organization': self.organization.name,
            'role': self.role,
            'active': self.active,
        }
        return value

    def set_role(self, role, should_activate=False):
        self.role = role.value
        if should_activate:
            self.active = True
        else:
            # do not change `active` status
            pass

        self.save()


class BaseAbstractOrganizationInvitation(HtkBaseModel):
    organization = fk_organization(related_name='invitations', required=True)
    invited_by = fk_user(
        related_name='organization_invitations_sent',
        required=True,
    )
    user = fk_user(
        related_name='organization_invitations',
    )
    email = models.EmailField(
        blank=True, null=True, default=None
    )  # email where invitation was originally sent
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    accepted = models.BooleanField(
        default=None, null=True
    )  # True: accepted, False: declined, None: not responded yet
    timestamp = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        abstract = True
        verbose_name = 'Organization Invitation'

    def __str__(self):
        value = '{organization_name} - {email} - {status}'.format(
            organization_name=self.organization.name,
            email=self.email,
            status=self.status,
        )
        return value

    def json_encode(self) -> Dict[str, Any]:
        """Returns a dictionary that can be `json.dumps()`-ed as a JSON representation of this object"""
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
            'Invited'
            if self.accepted is None
            else 'Accepted'
            if self.accepted
            else 'Declined'
        )

        return status

    ##
    # Notifications

    def _build_notification_message(self, subject, verb):
        msg = '{subject_name} ({subject_username}<{email}>) has {verb} an invitation for Organization <{organization_name}>'.format(  # noqa: E501
            verb=verb,
            subject_name=subject.profile.get_full_name(),
            subject_username=subject.username,
            email=subject.email,
            organization_name=self.organization.name,
        )
        return msg

    def build_notification_message__created(self):
        msg = self._build_notification_message(self.invited_by, 'sent')
        return msg

    def build_notification_message__resent(self):
        msg = self._build_notification_message(self.invited_by, 're-sent')
        return msg

    def build_notification_message__accepted(self):
        msg = self._build_notification_message(self.user, 'accepted')
        return msg

    def build_notification_message__declined(self):
        msg = self._build_notification_message(self.user, 'declined')
        return msg


class BaseAbstractOrganizationJoinRequest(HtkBaseModel):
    organization = fk_organization(related_name='join_requests', required=True)
    user = fk_user(
        related_name='organization_join_requests',
    )
    accepted = models.BooleanField(
        default=None, null=True
    )  # True: accepted, False: declined, None: not responded yet
    timestamp = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        abstract = True
        verbose_name = 'Organization Join Request'

    def __str__(self):
        value = '{organization_name} - {user} - {status}'.format(
            organization_name=self.organization.name,
            user=self.user,
            status=self.status,
        )
        return value

    def json_encode(self) -> Dict[str, Any]:
        """Returns a dictionary that can be `json.dumps()`-ed as a JSON representation of this object"""
        value = {
            'id': self.id,
            'organization': self.organization.name,
            'user': self.user.profile.get_full_name() if self.user else None,
            'accepted': self.accepted,
            'requested_at': self.timestamp,
            'responded_at': self.responded_at,
        }
        return value

    ##
    # properties

    @property
    def status(self) -> str:
        status = (
            'Requested'
            if self.accepted is None
            else 'Accepted' if self.accepted else 'Declined'
        )

        return status

    ##
    # Notifications

    def _build_notification_message(self, subject, action):
        msg = '{subject_name} ({subject_username}<{subject_email}>) request to join Organization <{organization_name}> has been {action}.'.format(  # noqa: E501
            action=action,
            subject_name=subject.profile.get_full_name(),
            subject_username=subject.username,
            subject_email=subject.email,
            organization_name=self.organization.name,
        )
        return msg

    def build_notification_message__created(self):
        msg = self._build_notification_message(self.user, 'sent')
        return msg

    def build_notification_message__accepted(self):
        msg = self._build_notification_message(self.user, 'accepted')
        return msg

    def build_notification_message__declined(self):
        msg = self._build_notification_message(self.user, 'declined')
        return msg


class BaseAbstractOrganizationTeam(HtkBaseModel):
    name = models.CharField(max_length=128)
    organization = fk_organization(related_name='teams', required=True)

    class Meta:
        abstract = True
        verbose_name = 'Organization Team'

    def __str__(self):
        value = '%s (%s)' % (
            self.name,
            self.organization.name,
        )
        return value

    ##
    # Accessors

    def get_members(self):
        sort_order = htk_setting('HTK_ORGANIZATION_TEAM_MEMBERS_SORT_ORDER')
        members = self.members.filter(
            # active=True, # TODO: exclude users that are not active at the organization level
            user__is_active=True
        ).order_by(*sort_order)
        return members


class BaseAbstractOrganizationTeamMember(HtkBaseModel):
    user = fk_user(related_name='organization_teams', required=True)
    team = models.ForeignKey(
        htk_setting('HTK_ORGANIZATION_TEAM_MODEL'),
        on_delete=models.CASCADE,
        related_name='members',
    )
    role = models.PositiveIntegerField(
        default=OrganizationTeamMemberRoles.MEMBER.value,
        choices=get_organization_team_member_role_choices(),
    )

    class Meta:
        abstract = True
        unique_together = (
            'user',
            'team',
        )
        verbose_name = 'Organization Team Member'

    def __str__(self):
        value = '%s - %s' % (
            self.user,
            self.team.__str__(),
        )
        return value


class BaseAbstractOrganizationTeamPosition(HtkBaseModel):
    name = models.CharField(max_length=128)
    team = models.ForeignKey(
        htk_setting('HTK_ORGANIZATION_TEAM_MODEL'),
        on_delete=models.CASCADE,
        related_name='positions',
    )

    class Meta:
        abstract = True
        unique_together = (
            'name',
            'team',
        )
        verbose_name = 'Organization Team Position'

    def __str__(self):
        value = '%s - %s' % (
            self.name,
            self.team.__str__(),
        )
        return value


class BaseAbstractOrganizationTeamMemberPosition(HtkBaseModel):
    member = models.ForeignKey(
        htk_setting('HTK_ORGANIZATION_TEAM_MEMBER_MODEL'),
        on_delete=models.CASCADE,
        related_name='positions',
    )
    position = models.ForeignKey(
        htk_setting('HTK_ORGANIZATION_TEAM_POSITION_MODEL'),
        on_delete=models.CASCADE,
        related_name='team_members',
    )

    class Meta:
        abstract = True
        verbose_name = 'Organization Team Member Position'

    def __str__(self):
        value = '%s - %s' % (
            self.position.name,
            self.member.__str__(),
        )
        return value
