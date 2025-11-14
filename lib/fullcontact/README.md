# Fullcontact Integration

Contact enrichment and identity verification.

## Quick Start

```python
from htk.lib.fullcontact.utils import find_person_by_email

person = find_person_by_email('user@example.com')
print(person.name, person.emails, person.phones)
```

## Operations

```python
from htk.lib.fullcontact.api import FullContactAPIV3

api = FullContactAPIV3()

# Get person by email
person = api.get_person(email='user@example.com')

# Get batch of people
people = api.get_persons(emails=['user1@example.com', 'user2@example.com'])

# Find valid emails
valid_emails = api.find_valid_emails(email_list)

# Format for Slack
slack_message = person.as_slack_v3()
```

## Configuration

```python
# settings.py
FULLCONTACT_API_KEY = os.environ.get('FULLCONTACT_API_KEY')
```
