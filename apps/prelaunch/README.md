# Prelaunch

## Functions
- **`prelaunch_toggle_view`** (prelaunch/api/views.py) - Toggle the early access status of a PrelaunchSignup
- **`get_or_create_by_email`** (prelaunch/models/base.py) - Gets or creates a `PrelaunchSignup` object by `email` and `site`
- **`notification_message`** (prelaunch/models/base.py) - Returns a message for Slack notifications about platform activity
- **`is_prelaunch_exception_view`** (prelaunch/utils.py) - Determines if the path is an excepted view from prelaunch redirection
- **`get_unique_signups`** (prelaunch/utils.py) - Returns a list of PrelaunchSignup objects with unique emails,

## Components
**Views** (`views.py`)
