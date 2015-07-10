import time
import tweepy
import twitter

from django.conf import settings

def get_twitter_api():
    api = twitter.Api(
        consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
        consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
        access_token_key=settings.SOCIAL_AUTH_TWITTER_ACCESS_TOKEN,
        access_token_secret=settings.SOCIAL_AUTH_TWITTER_ACCESS_TOKEN_SECRET
    )
    return api

def get_tweepy_api():
    consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY
    consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET
    access_token_key=settings.SOCIAL_AUTH_TWITTER_ACCESS_TOKEN
    access_token_secret=settings.SOCIAL_AUTH_TWITTER_ACCESS_TOKEN_SECRET
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)
    return api

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
    api = get_twitter_api()
    friends = api.GetFriends(screen_name=screen_name)
    return friends

def get_followers(screen_name):
    api = get_twitter_api()
    followers = api.GetFollowers(screen_name=screen_name)
    return followers

def get_followers_ids(screen_name):
    api = get_tweepy_api()
    ids = []
    is_first = True
    for page in tweepy.Cursor(api.followers_ids, screen_name=screen_name).pages():
        if not is_first:
            time.sleep(60)
        else:
            is_first = False
        ids.extend(page)
    return ids
