from htk.apps.organizations.enums import OrganizationMemberRoles
from htk.apps.organizations.enums import OrganizationTeamMemberRoles
from htk.models import AbstractAttribute
from htk.models import AbstractAttributeHolderClassFactory
from htk.models import HtkBaseModel
from htk.utils import htk_setting

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
    holder_resolver=lambda self: self.organization
).get_class()

class BaseAbstractOrganization(HtkBaseModel, OrganizationAttributeHolder):
    name = models.CharField(max_length=128)
    handle = models.CharField(unique=True)

    class Meta:
        abstract = True

class BaseAbstractOrganizationMember(HtkBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='organizations')
    organization = models.ForeignKey(htk_setting('HTK_ORGANIZATION_MODEL'), related_name='members')
    role = models.PositiveIntegerField(default=OrganizationMemberRoles.MEMBER.value)

    class Meta:
        abstract = True

class BaseAbstractOrganizationInvitation(HtkBaseModel):
    organization = models.ForeignKey(htk_setting('HTK_ORGANIZATION_MODEL'), related_name='invitations')
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='organization_invitations_sent')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='organization_invitations', blank=True, null=True, default=None)
    email = models.EmailField(blank=True, null=True, default=None)
    accepted = models.NullBooleanField(default=None) # True: accepted, False: declined, None: not responded yet
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class BaseAbstractOrganizationTeam(HtkBaseModel):
    name = models.CharField(max_length=128)
    organization = models.ForeignKey(htk_setting('HTK_ORGANIZATION_MODEL'), related_name='teams')

    class Meta:
        abstract = True

class BaseAbstractOrganizationTeamMember(HtkBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='organization_teams')
    team = models.ForeignKey(htk_setting('HTK_ORGANIZATION_TEAM_MODEL'), related_name='members')
    role = models.PositiveIntegerField(default=OrganizationTeamMemberRoles.MEMBER.value)

    class Meta:
        abstract = True
        unique_together = ('user', 'team',)
