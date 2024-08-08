HTK_ACCOUNTS_DEFAULT_DISPLAY_NAME = 'User'
HTK_ACCOUNTS_CONFIRM_EMAIL_URL_NAME = 'account_confirm_email'

HTK_API_USERS_FOLLOW_URL_NAME = 'api_users_follow'
HTK_API_USERS_UNFOLLOW_URL_NAME = 'api_users_unfollow'

HTK_DEFAULT_LOGGED_IN_ACCOUNT_HOME = 'account_index'

HTK_ACCOUNTS_CHANGE_PASSWORD_UPDATE_SESSION_AUTH_HASH = True

HTK_ACCOUNTS_REGISTER_SET_PRETTY_USERNAME_FROM_EMAIL = False
HTK_ACCOUNTS_REGISTER_SOCIAL_LOGIN_URL_NAME = 'account_register_social_login'
HTK_ACCOUNTS_REGISTER_SOCIAL_EMAIL_URL_NAME = 'account_register_social_email'
HTK_ACCOUNTS_REGISTER_SOCIAL_ALREADY_LINKED_URL_NAME = (
    'account_register_social_already_linked'
)
HTK_ACCOUNTS_REGISTER_SOCIAL_EMAIL_AND_TERMS_URL_NAME = (
    'account_register_social_email_and_terms'
)
HTK_ACCOUNTS_RESET_PASSWORD_URL_NAME = 'account_reset_password'
HTK_ACCOUNTS_RESEND_CONFIRMATION = 'account_resend_confirmation'

HTK_USER_PROFILE_MODEL = None

HTK_VALID_USERNAME_REGEX = r'^[A-Za-z0-9_-]{1,30}$'
HTK_USERNAME_HELP_TEXT = (
    'Required. 30 characters or fewer. Letters, digits and -/_ only.'
)

HTK_ACCOUNT_ACTIVATION_REMINDER_EMAIL_TEMPLATE = 'accounts/activation_reminder'

HTK_ACCOUNT_ACTIVATE_UPON_REGISTRATION = False

##
# Auth and Security

HTK_USER_ID_XOR = 314159265

HTK_USER_TOKEN_AUTH_ENCRYPTION_KEY = 'htk:someRandomCryptoKey'
HTK_USER_TOKEN_AUTH_EXPIRES_MINUTES = 15

##
# Account Email Subjects
HTK_ACCOUNT_EMAIL_SUBJECT_ACTIVATION = 'Confirm your email address, %(email)s'
HTK_ACCOUNT_EMAIL_SUBJECT_PASSWORD_CHANGED = 'Password changed on %(site_name)s'
HTK_ACCOUNT_EMAIL_SUBJECT_PASSWORD_RESET = 'Password reset on %(site_name)s'
HTK_ACCOUNT_EMAIL_SUBJECT_WELCOME = 'Welcome to %(site_name)s, %(email)s'

##
# Account Email BCC
HTK_ACCOUNT_EMAIL_BCC_ACTIVATION = True
HTK_ACCOUNT_EMAIL_BCC_WELCOME = True

##
# User Attributes
HTK_USER_ATTRIBUTE_DEFAULTS = {}

##
# Social Auth

HTK_SOCIAL_AUTH_PROVIDERS = [
    'discord',
    'facebook',
    'fitbit',
    'github',
    'google-oauth2',
    'linkedin-oauth2',
    'strava',
    'twitter',
]

HTK_SOCIAL_AUTH_LOGIN_PROVIDERS = [
    'discord',
    'facebook',
    'fitbit',
    'github',
    'google-oauth2',
    'linkedin-oauth2',
    'strava',
    'twitter',
]
