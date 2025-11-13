# Yahoo Integration

Yahoo services including finance, sports, and groups.

## Quick Start

```python
from htk.lib.yahoo.finance.utils import get_stock_price, get_stock_info_and_historical_data
from htk.lib.yahoo.sports.fantasy.utils import get_yahoo_fantasy_sports_client_for_user

# Get stock price
price = get_stock_price('AAPL')

# Get stock info and history
info = get_stock_info_and_historical_data('AAPL')

# Get fantasy sports client
client = get_yahoo_fantasy_sports_client_for_user(user)
leagues = client.get_user_leagues(user_id)
rosters = client.get_user_leagues_rosters(user_id)
```

## Configuration

```python
# settings.py
YAHOO_API_KEY = os.environ.get('YAHOO_API_KEY')
YAHOO_OAUTH_CLIENT_ID = os.environ.get('YAHOO_OAUTH_CLIENT_ID')
YAHOO_OAUTH_CLIENT_SECRET = os.environ.get('YAHOO_OAUTH_CLIENT_SECRET')
```

## Related Modules

- `htk.lib.twitter` - Social media APIs
