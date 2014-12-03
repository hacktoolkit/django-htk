import time

from rauth import OAuth1Service
from rauth.service import process_token_request
from rauth.utils import parse_utf8_qsl

YAHOO_OAUTH_REQUEST_TOKEN_URL = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
YAHOO_OAUTH_ACCESS_TOKEN_URL = 'https://api.login.yahoo.com/oauth/v2/get_token'
YAHOO_OAUTH_AUTHORIZE_URL = 'https://api.login.yahoo.com/oauth/v2/request_auth'

class YahooOAuthClient(object):
    def __init__(self, app_key, app_secret, user_social_auth):
        """Constructor for YahooOAuthClient

        `app_key` - Yahoo App Key
        `app_secret` - Yahoo App Secret
        `user_social_auth` - UserSocialAuth model to store refreshed token
        """
        # UserSocialAuth needed to access the access token
        self.last_error = None
        self.user_social_auth = user_social_auth
        self.access_token = user_social_auth.extra_data.get('access_token')
        self.oauth = OAuth1Service(
                name='Yahoo',
                consumer_key=app_key,
                consumer_secret=app_secret,
                request_token_url=YAHOO_OAUTH_REQUEST_TOKEN_URL,
                access_token_url=YAHOO_OAUTH_ACCESS_TOKEN_URL,
                authorize_url=YAHOO_OAUTH_AUTHORIZE_URL,
            )
        self.session = self.oauth.get_session((self.access_token['oauth_token'], self.access_token['oauth_token_secret']))

    def refresh_token_if_needed(func):
        """Decorator to make sure we refresh the token if needed before every query
        """
        def keys_from_response(text):
            return_array = []
            response_array = text.split('&')
            for e in response_array:
                pair = e.split('=', 2 )
                return_array.append(pair[0])
            return return_array

        def refresh(self, *args, **kwargs):
            # Let's refresh 5 minutes before the expiration time
            expires = self.user_social_auth.extra_data['expires']
            expires_time = int(expires) - 300 if expires else 0
            now = int(time.time())
            # print "comparing n: {0} vs expire: {1}".format(now, expires)
            if expires == None or expires < now:
                print "------ Refreshing Token ------"
                r = self.oauth.get_raw_access_token(
                    request_token=self.access_token["oauth_token"],
                    request_token_secret=self.access_token["oauth_token_secret"],
                    params={'oauth_session_handle':self.access_token["oauth_session_handle"]},
                )
                keys = keys_from_response(r.text)
                access_token = process_token_request(r, parse_utf8_qsl, *keys)
                for i,k in enumerate(keys):
                    self.access_token[k] = access_token[i]

                # Save back to UserSocialAuth Model
                self.user_social_auth.extra_data["access_token"] = self.access_token
                current_time = int(time.time())
                self.user_social_auth.extra_data["expires"] = current_time + int(self.access_token['oauth_expires_in'])
                # print "current time: {0}, expiring oauth at {1}".format(current_time, self.user_social_auth.extra_data["expires"])
                self.user_social_auth.save()

                token = (self.access_token['oauth_token'], self.access_token['oauth_token_secret'])
                self.session = self.oauth.get_session(token)
            return func(self, *args, **kwargs)
        return refresh
