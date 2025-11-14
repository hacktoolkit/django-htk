# Iterable Constants

Configuration settings for Iterable email and marketing automation integration.

## API Configuration

```python
from htk.lib.iterable.constants import (
    HTK_ITERABLE_API_KEY,
    HTK_ITERABLE_ENABLED,
)
```

**HTK_ITERABLE_API_KEY**
- API key for Iterable authentication
- Default: `None` (must be configured in settings)
- Required to enable Iterable integration

**HTK_ITERABLE_ENABLED**
- Boolean flag to enable/disable Iterable integration
- Default: `False`
- Set to `True` to activate email campaigns and workflows

## Campaign Configuration

```python
from htk.lib.iterable.constants import HTK_ITERABLE_CAMPAIGN_IDS
```

**HTK_ITERABLE_CAMPAIGN_IDS**
- Nested dictionary mapping campaign categories to campaign IDs
- Structure:
  - `'triggered'`: Triggered campaigns
    - `'transactional'`: Transactional emails
      - `'account'`: Account-related campaigns
        - `'sign_up_confirm_email'`: Sign-up confirmation campaign ID
        - `'confirm_email_resend'`: Email confirmation resend campaign ID
    - `'notifications'`: Notification campaigns
      - `'account'`: Account notifications
    - `'recurring'`: Recurring campaigns
- Default: Campaign IDs are `None` (must be configured)

## List and Workflow Configuration

```python
from htk.lib.iterable.constants import (
    HTK_ITERABLE_LIST_IDS,
    HTK_ITERABLE_WORKFLOW_IDS,
)
```

**HTK_ITERABLE_LIST_IDS**
- Dictionary mapping list names to Iterable list IDs
- Default: `{}` (empty, add your lists here)
- Used for subscribing/managing users on specific lists

**HTK_ITERABLE_WORKFLOW_IDS**
- Dictionary mapping workflow names to workflow IDs
- Workflows:
  - `'account.sign_up'`: New account signup workflow
  - `'account.activation'`: Account activation workflow
  - `'account.login'`: User login workflow
- Default: Workflow IDs are `None` (must be configured)

## Options

```python
from htk.lib.iterable.constants import HTK_ITERABLE_OPTIONS
```

**HTK_ITERABLE_OPTIONS**
- Configuration options for Iterable behavior
- Options:
  - `'override_welcome_email'`: Boolean to override default welcome email (default: `False`)

## Example Usage

```python
from htk.lib.iterable.constants import (
    HTK_ITERABLE_API_KEY,
    HTK_ITERABLE_CAMPAIGN_IDS,
    HTK_ITERABLE_WORKFLOW_IDS,
)

# Get campaign ID for sign-up confirmation
campaign_id = HTK_ITERABLE_CAMPAIGN_IDS['triggered']['transactional']['account']['sign_up_confirm_email']

# Get workflow ID for account signup
workflow_id = HTK_ITERABLE_WORKFLOW_IDS['account.sign_up']
```

## Configuration in settings.py

```python
HTK_ITERABLE_API_KEY = 'your_iterable_api_key'
HTK_ITERABLE_ENABLED = True

HTK_ITERABLE_CAMPAIGN_IDS = {
    'triggered': {
        'transactional': {
            'account': {
                'sign_up_confirm_email': 12345,
                'confirm_email_resend': 12346,
            },
        },
        'notifications': {
            'account': {},
        },
        'recurring': {},
    },
}

HTK_ITERABLE_LIST_IDS = {
    'newsletter': 98765,
    'customers': 98766,
}

HTK_ITERABLE_WORKFLOW_IDS = {
    'account.sign_up': 54321,
    'account.activation': 54322,
    'account.login': 54323,
}

HTK_ITERABLE_OPTIONS = {
    'override_welcome_email': False,
}
```
