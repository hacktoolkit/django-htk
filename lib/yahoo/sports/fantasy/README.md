# Fantasy

## Functions
- **`get`** (fantasy/client.py) - Extracts data from a JSON collection using path-based tree traversal
- **`perform_api_query`** (fantasy/client.py) - Wrapper for making a query to the Yahoo Fantasy Sports API
- **`get_user`** (fantasy/client.py) - Get Users collection along with any specified subresources
- **`get_user_leagues`** (fantasy/client.py) - `game_keys` - comma-separated list of game codes,
- **`get_user_leagues_keys`** (fantasy/client.py) - Get the league keys for every league this user has
- **`get_user_leagues_players`** (fantasy/client.py) - Get all of the players in all of the leagues this user has
- **`get_user_leagues_rosters`** (fantasy/client.py) - Get the rosters for every league this user has
- **`get_yahoo_fantasy_sports_client_for_user`** (fantasy/utils.py) - Gets a YahooFantasySportsAPIClient instance for `user`

## Components
**Views** (`views.py`)

## URL Patterns
- `index`
- `lib_yahoo_sports_fantasy_get_user`
- `lib_yahoo_sports_fantasy_get_user_leagues`
- `lib_yahoo_sports_fantasy_get_user_leagues_players`
- `lib_yahoo_sports_fantasy_get_user_leagues_rosters`
