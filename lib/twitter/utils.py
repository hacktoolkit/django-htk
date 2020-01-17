# Python Standard Library Imports
import time

# Third Party (PyPI) Imports
import rollbar
import tweepy

# HTK Imports
from htk.utils import chunks


def _get_auth_keys():
    from django.conf import settings
    consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY
    consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET
    access_token_key=settings.SOCIAL_AUTH_TWITTER_ACCESS_TOKEN
    access_token_secret=settings.SOCIAL_AUTH_TWITTER_ACCESS_TOKEN_SECRET
    auth_keys = (
        consumer_key,
        consumer_secret,
        access_token_key,
        access_token_secret,
    )
    return auth_keys

def get_api(consumer_key=None, consumer_secret=None, access_token_key=None, access_token_secret=None, wait_on_rate_limit=False):
    from htk.lib.twitter.api import HtkTwitterAPI
    api = HtkTwitterAPI(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token_key=access_token_key,
        access_token_secret=access_token_secret,
        wait_on_rate_limit=wait_on_rate_limit
    )
    return api

def get_twitter_api(consumer_key=None, consumer_secret=None, access_token_key=None, access_token_secret=None, wait_on_rate_limit=False):
    import twitter
    if not(all((consumer_key, consumer_secret, access_token_key, access_token_secret,))):
        (consumer_key, consumer_secret, access_token_key, access_token_secret,) = _get_auth_keys()
    api = twitter.Api(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token_key=access_token_key,
        access_token_secret=access_token_secret
    )
    return api

def get_tweepy_api(consumer_key=None, consumer_secret=None, access_token_key=None, access_token_secret=None, wait_on_rate_limit=False):
    if not(all((consumer_key, consumer_secret, access_token_key, access_token_secret,))):
        (consumer_key, consumer_secret, access_token_key, access_token_secret,) = _get_auth_keys()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=wait_on_rate_limit)
    return api

def get_user(screen_name):
    api = get_tweepy_api()
    twitter_user = api.get_user(screen_name=screen_name)
    return twitter_user

def lookup_users_by_id(user_ids):
    """
    https://dev.twitter.com/rest/reference/get/users/lookup

    Requests / 15-min window (app auth): 60
    """
    api = get_tweepy_api()
    users = []
    for chunk in chunks(user_ids, 100):
        users.extend(api.lookup_users(user_ids=chunk))
        time.sleep(15)
    return users

def get_lists(screen_name):
    api = get_tweepy_api()
    lists = api.lists_all(screen_name)
    return lists

def get_lists_with_members(screen_name):
    api = get_twitter_api()
    lists = get_lists(screen_name)
    lists_with_members = []
    for l in lists:
        list_obj = {}
        list_obj['list'] = l
        list_id = l.id
        list_members = api.GetListMembers(list_id, None)
        list_obj['members'] = list_members
        lists_with_members.append(list_obj)
    return lists_with_members

def get_lists_members_deduped(screen_name):
    api = get_twitter_api()
    lists = get_lists(screen_name)
    members_dict = {}
    for l in lists:
        list_id = l.id
        list_members = api.GetListMembers(list_id, None)
        for member in list_members:
            members_dict[member.screen_name] = True
    members = sorted(members_dict.keys())
    return members

def get_following(screen_name):
    friends = get_friends(screen_name)
    return friends

def get_friends(screen_name):
    """
    https://dev.twitter.com/rest/reference/get/friends/list

    Requests / 15-min window (app auth): 30
    """
    api = get_tweepy_api()
    friends = []
    is_first = True
    for page in tweepy.Cursor(api.friends, screen_name=screen_name, count=200).pages():
        if not is_first:
            time.sleep(30)
        else:
            is_first = False
        friends.extend(page)
    return friends
#    api = get_twitter_api()
#    friends = api.GetFriends(screen_name=screen_name, count=200)
#    return friends

def get_friends_ids(screen_name):
    api = get_tweepy_api()
    ids = []
    is_first = True
    try:
        for page in tweepy.Cursor(api.friends_ids, screen_name=screen_name, count=5000).pages():
            if not is_first:
                time.sleep(60)
            else:
                is_first = False
            ids.extend(page)
    except tweepy.RateLimitError:
        extra_data = {
            'screen_name' : screen_name,
        }
        rollbar.report_exc_info(extra_data=extra_data)
    return ids

def get_followers(screen_name):
    """
    https://dev.twitter.com/rest/reference/get/followers/list

    Requests / 15-min window (app auth): 30
    """
    api = get_twitter_api()
    followers = api.GetFollowers(screen_name=screen_name)
    return followers

def get_followers_ids(screen_name):
    """
    https://dev.twitter.com/rest/reference/get/followers/ids

    Requests / 15-min window (app auth): 15
    """
    api = get_tweepy_api()
    ids = []
    is_first = True
    try:
        for page in tweepy.Cursor(api.followers_ids, screen_name=screen_name, count=5000).pages():
            if not is_first:
                time.sleep(60)
            else:
                is_first = False
            ids.extend(page)
    except tweepy.RateLimitError:
        extra_data = {
            'screen_name' : screen_name,
        }
        rollbar.report_exc_info(extra_data=extra_data)
    return ids

def search_tweets(keyword, limit=None, api=None):
    """Get Tweet search results for `keyword`
    """
    if api is None:
        api = get_tweepy_api()
    tweet_results = api.search(
        q=keyword,
        count=limit,
        result_type='recent'
    )
    return tweet_results
