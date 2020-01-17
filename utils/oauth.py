# Third Party (PyPI) Imports
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth2Session


def get_twitter_oauth():
#    oauth = OAuth1(settings.TWITTER_CONSUMER_KEY,
#                client_secret=settings.TWITTER_CONSUMER_SECRET,
#                resource_owner_key=OAUTH_TOKEN,
#                resource_owner_secret=OAUTH_TOKEN_SECRET)
    oauth = OAuth2Session()
    return oauth
