# Yahoo

## Classes
- **`YahooGroupsMessage`** (yahoo/groups/message.py) - Represents a Yahoo Groups message

## Functions
- **`get_stock_info_and_historical_data`** (yahoo/finance/utils.py) - Retrieve stock info and historical data for `symbol`
- **`get_stock_price`** (yahoo/finance/utils.py) - Retrieve the latest price for `symbol` representing stock
- **`message`** (yahoo/groups/message.py) - Returns the main message text
- **`yahoo_groups_message_parser`** (yahoo/groups/utils.py) - Extracts the main message from a Yahoo Groups message
- **`refresh_token_if_needed`** (yahoo/oauth.py) - Decorator to make sure we refresh the token if needed before every query
- **`refresh`** (yahoo/oauth.py) - `self` is an instance of YahooOAuthClient
- **`get`** (yahoo/sports/fantasy/client.py) - Extracts data from a JSON collection using path-based tree traversal
- **`perform_api_query`** (yahoo/sports/fantasy/client.py) - Wrapper for making a query to the Yahoo Fantasy Sports API
- **`get_user`** (yahoo/sports/fantasy/client.py) - Get Users collection along with any specified subresources
- **`get_user_leagues`** (yahoo/sports/fantasy/client.py) - `game_keys` - comma-separated list of game codes,
- **`get_user_leagues_keys`** (yahoo/sports/fantasy/client.py) - Get the league keys for every league this user has
- **`get_user_leagues_players`** (yahoo/sports/fantasy/client.py) - Get all of the players in all of the leagues this user has
- **`get_user_leagues_rosters`** (yahoo/sports/fantasy/client.py) - Get the rosters for every league this user has
- **`get_yahoo_fantasy_sports_client_for_user`** (yahoo/sports/fantasy/utils.py) - Gets a YahooFantasySportsAPIClient instance for `user`
