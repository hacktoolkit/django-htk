from django.conf import settings

class HtkTwitterAPI(object):
    def __init__(
        self,
        consumer_key=None,
        consumer_secret=None,
        access_token_key=None,
        access_token_secret=None
    ):
        if consumer_key is None:
            consumer_key = settings.SOCIAL_AUTH_TWITTER_KEY
        if consumer_secret is None:
            consumer_secret = settings.SOCIAL_AUTH_TWITTER_SECRET

        from htk.lib.twitter.utils import get_twitter_api
        from htk.lib.twitter.utils import get_tweepy_api
        self.twitter_api = get_twitter_api(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token_key,
            access_token_secret=access_token_secret
        )
        self.tweepy_api = get_tweepy_api(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token_key,
            access_token_secret=access_token_secret
        )

    ##
    # Friendship Methods

    def unfollow(self, id=None, screen_name=None, user_id=None):
        # http://tweepy.readthedocs.io/en/v3.5.0/api.html#API.destroy_friendship
        user = self.tweepy_api.destroy_friendship(id=id, screen_name=screen_name, user_id=user_id)
        return user
