from htk.utils.enums import get_enum_symbolic_name

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
