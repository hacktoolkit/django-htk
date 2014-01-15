import requests

from django import template

register = template.Library()

# https://dev.twitter.com/docs/api/1.1/get/users/show

URL_TWITTER_API_USERS_SHOW = 'https://api.twitter.com/1.1/users/show.json?user_id=%s'

def twitter_picture(twid):
    response = requests.get(URL_TWITTER_API_USERS_SHOW % twid)
    data = response.json()
    picture_url = data.get('profile_image_url', twid)
    return picture_url

register.simple_tag(twitter_picture)
