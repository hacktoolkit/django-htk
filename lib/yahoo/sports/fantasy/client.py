import json

from htk.lib.yahoo.oauth import YahooOAuthClient

class YahooFantasySportsAPIResponse(object):
    def __init__(self, json_data, *args, **kwargs):
        self.json_data = json_data

    def get_error(self):
        if self.json_data.has_key('error'):
            error = self.json_data['error']['description']
        else:
            error = None
        return error

    def _get_collection_item_key(self, collection_key):
        """Gets the collection item key for the `collection_key`
        Currently naively assumes plural with 's'

        E.g.
        'games' -> 'game'
        'users' -> 'user'
        """
        collection_item_key = collection_key[:-1]
        return collection_item_key

    def get(self, path):
        """Extracts data from a JSON collection using path-based tree traversal


        `path` is a tuple-pair of the collection key and the payload offset

        Returns a list of items designated by the path

        # ----- Sample Usage: -----
        # league_metadata = r.get(path=(('leagues', 0),))
        # for l in league_metadata:
        #     o = YahooResponseObject(l)
        #     fantasy_league = FantasyLeague.model_from_yahoo_response_object(o)
        #     fantasy_league.users.add(self.user)

        # players = r.get(path=(('leagues', 1), ('teams', 1), ('roster', 0), ('players', 0)))
        # for p in players:
        #     o = YahooResponseObject(p)
        #     # print(o.name['full'])
        """
        items = []
        path_length = len(path)
        stack = []
        # push the root node onto the stack
        # The outer dict always has the fantasy_content key
        stack.append((self.json_data['fantasy_content'], 0))
        while len(stack) > 0:
            (current_node, depth,) = stack.pop()
            (collection_key, payload_index,) = path[depth]
            if len(current_node[collection_key]) > 0:
                if current_node[collection_key].has_key('count'):
                    count = current_node[collection_key]['count']
                    collection_item_key = self._get_collection_item_key(collection_key)
                    for i in range(count):
                        child = current_node[collection_key][str(i)][collection_item_key][payload_index]
                        if depth + 1 == path_length:
                            # reached the leaf node (last element along path), which is the item we want
                            items.append(child)
                        else:
                            subnode = (child, depth + 1,)
                            stack.append(subnode)
                else:
                    # no 'count', so just append or return the dict
                    child = current_node[collection_key][str(payload_index)]
                    if depth + 1 == path_length:
                        # reached the leaf node (last element along path), which is the item we want
                        items.append(child)
                    else:
                        subnode = (child, depth + 1,)
                        stack.append(subnode)
            else:
                # current_node[collection_key] is empty
                pass

        return items

    def __str__ (self):
        value = json.dumps(self.json_data, indent=2)
        return value


from htk.lib.yahoo.oauth import refresh_token_if_needed


class YahooFantasySportsAPIClient(YahooOAuthClient):
    BASE_URL = 'http://fantasysports.yahooapis.com/fantasy/v2/'

    @refresh_token_if_needed
    def perform_api_query(self, resource):
        """Wrapper for making a query to the Yahoo Fantasy Sports API

        `resource` is the resource that we want to get
        """
        uri = '%s%s' % (self.BASE_URL, resource)
        response = self.session.get(uri, params={'format':'json'})
        parsed_response = YahooFantasySportsAPIResponse(json_data=response.json())
        if parsed_response and not self.last_error:
            result = parsed_response
        else:
            result = None
        return result

    def get_user(self, subresource=''):
        """Get Users collection along with any specified subresources

        https://developer.yahoo.com/fantasysports/guide/users-collection.html
        """
        resource = 'users;use_login=1'
        if subresource:
            resource = '%s/%s' % (resource, subresource)
        else:
            pass
        result = self.perform_api_query(resource)
        return result

    def get_user_leagues(self, game_keys='nfl,mlb,nba,nhl'):
        """
        `game_keys` - comma-separated list of game codes,
        default is to all full games for the current season

        game codes of full games: nfl, mlb, nba, nhl

        https://developer.yahoo.com/fantasysports/guide/league-resource.html#league-resource-desc
        """
        if game_keys:
            subresource = 'games;game_keys=%s/leagues' % game_keys
        else:
            subresource = 'games/leagues'

        result = self.get_user(subresource=subresource)
        return result

    def get_user_leagues_keys(self):
        """Get the league keys for every league this user has

        Returns a comma-separated list of league keys
        Returns empty string if no leagues available
        """
        leagues_response = self.get_user_leagues()
        if leagues_response:
            path = (
                ('users', 1),
                ('games', 1),
                ('leagues', 0),
            )
            leagues = leagues_response.get(path)
            league_keys = [league_dict['league_key'] for league_dict in leagues]
            league_keys_str = ','.join(league_keys)
        else:
            league_keys = ''

        return league_keys_str

    def get_user_leagues_players(self):
        """Get all of the players in all of the leagues this user has

        https://developer.yahoo.com/fantasysports/guide/players-collection.html#players-collection-desc
        """
        league_keys_str = self.get_user_leagues_keys()
        resource = 'leagues;league_keys=%s/players' % league_keys_str
        result = self.perform_api_query(resource)
        return result

    def get_user_leagues_rosters(self):
        """Get the rosters for every league this user has

        https://developer.yahoo.com/fantasysports/guide/roster-resource.html#roster-resource-desc
        """
        league_keys_str = self.get_user_leagues_keys()
        resource = 'leagues;league_keys=%s/teams/roster' % league_keys_str
        result = self.perform_api_query(resource)
        return result
