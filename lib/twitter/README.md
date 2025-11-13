# Twitter Integration

Twitter API for tweets, users, and social data.

## Quick Start

```python
from htk.lib.twitter.utils import search_tweets, lookup_users_by_id, get_followers

# Search tweets
results = search_tweets(keyword='#python')

# Look up users
users = lookup_users_by_id([123456, 789012])

# Get followers
followers = get_followers(user_id='12345')

# Get followers IDs
follower_ids = get_followers_ids(user_id='12345')
```

## Configuration

```python
# settings.py
TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
```

## Related Modules

- `htk.lib.facebook` - Social media APIs
- `htk.lib.linkedin` - Professional networking
