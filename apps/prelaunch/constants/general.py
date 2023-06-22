HTK_PRELAUNCH_MODE = False
HTK_PRELAUNCH_HOST_REGEXPS = [
#    r'(dev|qa|alpha)\.hacktoolkit\.com',
#    r'demo\.hacktoolkit\.com',
]
HTK_PRELAUNCH_URL_NAME = 'htk_prelaunch'

# a list of views for which we ignore prelaunch redirection
# a string that can be reversed
HTK_PRELAUNCH_EXCEPTION_VIEWS = (
    HTK_PRELAUNCH_URL_NAME,
    'htk_feedback_submit',
    # meta/seo
    'bing_site_auth',
    'robots',
    'django.contrib.sitemaps.views.sitemap',
)

# a list of url regexps for which we ignore prelaunch redirection
HTK_PRELAUNCH_EXCEPTION_URLS = (
    # meta/seo
    r'^/google[a-z0-9]+\.html$', # google_site_verification
    r'^/.+--\.html$', # html_site_verification
    # admin
    r'^/admin/',
    r'^/htkadmin/',
)

HTK_PRELAUNCH_TEMPLATE = 'htk/prelaunch.html'

HTK_PRELAUNCH_EMAIL_TEMPLATE = 'htk/prelaunch'
HTK_PRELAUNCH_EMAIL_SUBJECT = 'Thanks for signing up'
HTK_PRELAUNCH_EMAIL_BCC = []
