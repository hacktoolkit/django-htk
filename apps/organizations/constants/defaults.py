HTK_ORGANIZATION_MODEL = 'organizations.Organization'
HTK_ORGANIZATION_ATTRIBUTE_MODEL = 'organizations.OrganizationAttribute'
HTK_ORGANIZATION_MEMBER_MODEL = 'organizations.OrganizationMember'
HTK_ORGANIZATION_INVITATION_MODEL = 'organizations.OrganizationInvitation'
HTK_ORGANIZATION_TEAM_MODEL = 'organizations.OrganizationTeam'
HTK_ORGANIZATION_TEAM_MEMBER_MODEL = 'organizations.OrganizationTeamMember'
HTK_ORGANIZATION_TEAM_POSITION_MODEL = 'organizations.OrganizationTeamPosition'
HTK_ORGANIZATION_TEAM_MEMBER_POSITION_MODEL = 'organizations.OrganizationTeamMemberPosition'

HTK_ORGANIZATION_MEMBERS_SORT_ORDER = (
    'user__first_name',
    'user__last_name',
    'user__username',
)

HTK_ORGANIZATION_TEAM_MEMBERS_SORT_ORDER = (
    'user__first_name',
    'user__last_name',
    'user__username',
)
