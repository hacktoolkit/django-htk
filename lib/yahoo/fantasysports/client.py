import json

from htk.lib.yahoo.oauth import YahooOAuthClient

class YahooFantasySportsAPIResponse(object):
    def __init__(self, json_data, *args, **kwargs):
        self.json_data = json_data

    def get_error(self):
        if self.json_data.has_key('error'):
            return self.json_data['error']['description']
        else:
            return None

    # ----- Sample Usage: -----
    # league_metadata = r.get(path=(('leagues', 0),))
    # for l in league_metadata:
    #     o = YahooResponseObject(l)
    #     fantasy_league = FantasyLeague.model_from_yahoo_response_object(o)
    #     fantasy_league.users.add(self.user)

    # players = r.get(path=(('leagues',1), ('teams', 1), ('roster', 0), ('players',0)))
    # for p in players:
    #     o = YahooResponseObject(p)
    #     # print o.name['full']

    def get(self, path):
        return_array = []
        path_length = len(path)
        stack = []
        # The outer dict alwayas has the fantasy_content key
        stack.append((self.json_data["fantasy_content"], 0))
        while len(stack) > 0:
            current_dict, path_index = stack.pop()
            collection_key, array_index = path[path_index]
            if len(current_dict[collection_key]) > 0:
                if current_dict[collection_key].has_key("count"):
                    count = current_dict[collection_key]["count"]
                    for i in range(0,count):
                        if path_index == path_length-1:
                            return_array.append(current_dict[collection_key][str(i)][collection_key[:-1]][array_index])
                        else:
                            stack.append((current_dict[collection_key][str(i)][collection_key[:-1]][array_index], path_index+1))
                else:
                    # no count, so just append or return the dict
                    if path_index == path_length - 1:
                        return_array.append(current_dict[collection_key][str(array_index)])
                    else:
                        stack.append((current_dict[collection_key][str(array_index)], path_index+1))

        return return_array

    def __str__ (self):
        return json.dumps(self.json_data, indent=2)

class YahooFantasySportsAPIClient(YahooOAuthClient):
    BASE_URL = 'http://fantasysports.yahooapis.com/fantasy/v2/'

    @refresh_token_if_needed
    def api_query(self, url):
        response = self.session.get(url, params={'format':'json'})
        return YahooFantasySportsAPIResponse(json_data=response.json())

    def get_user_rosters(self):
        r = self.get_user_leagues()
        if r == None: return None
        leagues = r.get(path=(('users',1),('games',1),('leagues',0)))
        league_keys = map(lambda x: x["league_key"], leagues)
        url = self.BASE_URL+"leagues;league_keys={0}/teams/roster".format(','.join(league_keys))
        r = self.api_query(url)
        self.last_error = r.get_error()
        if r and not self.last_error:
            return r
        else:
            return None

    # Need to convert
    def get_user_leagues(self):
        url = self.BASE_URL + "users;use_login=1/games;game_keys=nba,nfl/leagues"
        r = self.api_query(url)
        self.last_error = r.get_error()
        if r and not self.last_error:
            return r
        else:
            return None
