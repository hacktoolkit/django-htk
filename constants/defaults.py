##
# Allowed hosts
HTK_ALLOWED_HOST_REGEXPS = (
    # TODO: remove this rule, it's too permissive
    r'(.*)',
    # e.g.
    #r'(.*\.)?hacktoolkit\.com(\.)?',
)

##
# Miscellaneous settings
HTK_SITE_NAME = 'Hacktoolkit'
HTK_SYMBOLIC_SITE_NAME = 'hacktoolkit'

HTK_INDEX_URL_NAME = 'index'
HTK_REDIRECT_URL_NAME = 'redir'

HTK_STATIC_META_TITLE_VALUES = {}
HTK_STATIC_META_DESCRIPTION_VALUES = {}

##
# Email settings
HTK_DEFAULT_EMAIL_SENDING_DOMAIN = 'hacktoolkit.com'
HTK_DEFAULT_EMAIL_SENDER = 'Hacktoolkit <no-reply@hacktoolkit.com>'
HTK_DEFAULT_EMAIL_RECIPIENTS = ['info@hacktoolkit.com',]

##
# Locale
HTK_DEFAULT_COUNTRY = 'US'
HTK_DEFAULT_TIMEZONE = 'America/Los_Angeles'

##
# Domain Verification URLs
HTK_DOMAIN_META_URL_NAMES = (
    'robots',
    'google_site_verification',
    'bing_site_auth',
    'sitemap',
)

##
# Enums
HTK_ENUM_SYMBOLIC_NAME_OVERRIDES = {}

from htk.apps.accounts.constants.defaults import *
from htk.apps.file_storage.constants.defaults import *
from htk.apps.invoices.constants.defaults import *
from htk.cache.constants.defaults import *
from htk.forms.constants.defaults import *
from htk.lib.qrcode.constants.defaults import *
from htk.lib.stripe_lib.constants.defaults import *
