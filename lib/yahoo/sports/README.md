# Sports

## Functions
- **`get`** (sports/fantasy/client.py) - Extracts data from a JSON collection using path-based tree traversal
- **`perform_api_query`** (sports/fantasy/client.py) - Wrapper for making a query to the Yahoo Fantasy Sports API
- **`get_user`** (sports/fantasy/client.py) - Get Users collection along with any specified subresources
- **`get_user_leagues`** (sports/fantasy/client.py) - `game_keys` - comma-separated list of game codes,
- **`get_user_leagues_keys`** (sports/fantasy/client.py) - Get the league keys for every league this user has
- **`get_user_leagues_players`** (sports/fantasy/client.py) - Get all of the players in all of the leagues this user has
- **`get_user_leagues_rosters`** (sports/fantasy/client.py) - Get the rosters for every league this user has
- **`get_yahoo_fantasy_sports_client_for_user`** (sports/fantasy/utils.py) - Gets a YahooFantasySportsAPIClient instance for `user`
