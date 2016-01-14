from htk.utils.enums import get_enum_symbolic_name

def get_organization_type_choices():
    from htk.apps.customers.enums import OrganizationType
    choices = [(organization_type.value, get_enum_symbolic_name(organization_type),) for organization_type in OrganizationType]
    return choices
