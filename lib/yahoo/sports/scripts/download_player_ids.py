from bs4 import BeautifulSoup
import re
import requests
import time

SPORTS = ['nfl', 'mlb', 'nba', 'nhl',]
LETTERS = [chr(x) for x in xrange(ord('A'), ord('Z') + 1)]

PLAYERS_BASE_URL = 'http://sports.yahoo.com/%(sport)s/players?type=lastname&query=%(letter)s'

class YahooSportsPlayer(object):
    def __init__(self):
        pass

    @classmethod
    def player_from_table_row(cls, tr):
        player = YahooSportsPlayer()
        fields = tr.find_all('td')
        #<tr class="ysprow1">
        # <td><a href="/nfl/players/9282">Robert Ayers Jr.</a></td>
        # <td>DE</td>
        # <td><a href="/nfl/teams/nyg">New York Giants</a></td>
        #</tr>
        player_link = fields[0].a
        if player_link:
            matches = re.match(r'.*\/(\d+)$', player_link['href'])
            player_id = matches.group(1).strip()
        else:
            return None

        player_name = fields[0].get_text().strip()
        position = fields[1].get_text().strip()
        team_link = fields[2].a['href']
        matches = re.match(r'.*\/([a-z]+)$', team_link)
        team_abbrev = matches.group(1).strip()
        team_name = fields[2].get_text().strip()

        player.player_id = player_id
        player.player_name = player_name
        player.position = position
        player.team_abbrev = team_abbrev
        player.team_name = team_name
        return player

    def __str__(self):
        value = self.__unicode__()
        return value

    def __unicode__(self):
        value = u'%s::%s::%s::%s::%s' % (
            self.player_id,
            self.player_name,
            self.position,
            self.team_abbrev,
            self.team_name,
        )
        return value

def download_players(sport, letter):
    uri = PLAYERS_BASE_URL % {
        'sport' : sport,
        'letter' : letter,
    }
    response = requests.get(uri)
    html = response.text
    soup = BeautifulSoup(html)
    table_rows = soup.find_all('tr')
    players = []
    for row in table_rows:
        row_class = row.get('class')[0] if row.get('class') else None
        if row_class in ('ysprow1', 'ysprow2',):
            # this is a player row
            player = YahooSportsPlayer.player_from_table_row(row)
            players.append(player)
        else:
            pass
    return players

if __name__ == '__main__':
    for sport in SPORTS:
        print(sport)
        for letter in LETTERS:
            players = download_players(sport, letter)
            for player in players:
                try:
                    print(player)
                except:
                    pass
        time.sleep(0.2)
