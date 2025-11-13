# Organizations

## Classes
- **`require_organization_permission`** (organizations/decorators.py) - Decorator for requiring current logged-in user to have required level of permission in Organization.
- **`OrganizationInvitationResponseView`** (organizations/views.py) - Organization Invitation Response Class Based View

## Functions
- **`organization_invitation_created_or_updated`** (organizations/apps.py) - Signal handler for when a new OrganizationInvitation object is created or updated
- **`send_invitation_email`** (organizations/emailers.py) - Sends invitation E-mail to given person
- **`json_encode`** (organizations/models.py) - Returns a dictionary that can be `json.dumps()`-ed as a JSON representation of this object
- **`get_members`** (organizations/models.py) - Returns all active members of this organization
- **`get_owners`** (organizations/models.py) - Returns all active owners of this organization
- **`json_encode`** (organizations/models.py) - Returns a dictionary that can be `json.dumps()`-ed as a JSON representation of this object
- **`json_encode`** (organizations/models.py) - Returns a dictionary that can be `json.dumps()`-ed as a JSON representation of this object
- **`accept`** (organizations/models.py) - Accept the organization invitation
- **`decline`** (organizations/models.py) - Decline the organization invitation
- **`json_encode`** (organizations/models.py) - Returns a dictionary that can be `json.dumps()`-ed as a JSON representation of this object
- **`invite_organization_member`** (organizations/utils.py) - Invite person to organization

## Components
**Views** (`views.py`)
