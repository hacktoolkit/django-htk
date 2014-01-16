##
# Allowed hosts
HTK_ALLOWED_HOST_REGEXPS = (
    # TODO: remove this rule, it's too permissive
    r'(.*)',
    # e.g.
    #r'(.*\.)?hacktoolkit\.com(\.)?',
)

##
# Email settings
HTK_DEFAULT_EMAIL_SENDING_DOMAIN = 'hacktoolkit.com'
HTK_DEFAULT_EMAIL_SENDER = 'Hacktoolkit <no-reply@hacktoolkit.com>'
HTK_DEFAULT_EMAIL_RECIPIENTS = ['info@hacktoolkit.com',]

##
# Locale
HTK_DEFAULT_COUNTRY = 'US'
HTK_DEFAULT_TIMEZONE = 'America/Los_Angeles'

from htk.apps.accounts.constants.defaults import *
from htk.cache.constants.defaults import *
