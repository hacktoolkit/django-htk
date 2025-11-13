# Invitations

## Functions
- **`get_relative_time`** (invitations/models.py) - Returns a string representing the relative duration of time between now and when the invitation was created
- **`connect_user`** (invitations/models.py) - Connects `user` to this `Invitation`
- **`complete`** (invitations/models.py) - Completes the invitation lifecycle
- **`process_user_created`** (invitations/services.py) - Invoked when `user` is created
- **`process_user_email_confirmation`** (invitations/services.py) - Invoked when `user_email` is confirmed
- **`process_user_completed`** (invitations/services.py) - Invoked when `user` completely satisfies the onboarding requirements of the invitation flow
