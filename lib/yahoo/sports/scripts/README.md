# Yahoo Sports Player Data Scripts

Scripts and utilities for downloading and parsing Yahoo Sports player data.

## Classes

**YahooSportsPlayer**
- Represents a Yahoo Sports player with career information
- Attributes: `player_id`, `player_name`, `position`, `team_abbrev`, `team_name`
- Factory method: `player_from_table_row(tr)` - Creates player from HTML table row

## Functions

**download_players(sport, letter)**
- Downloads Yahoo Sports players for a specific sport and starting letter
- Supports sports: `nfl`, `mlb`, `nba`, `nhl`
- Returns list of YahooSportsPlayer objects
- Uses BeautifulSoup to parse HTML response
- Filters rows by CSS class `ysprow1` and `ysprow2`

## Example Usage

```python
from htk.lib.yahoo.sports.scripts.download_player_ids import (
    download_players,
    YahooSportsPlayer,
)

# Download all NFL players starting with 'A'
players = download_players('nfl', 'A')

for player in players:
    print(f"{player.player_name} - {player.position} ({player.team_abbrev})")
    # Example: "Aaron Rodgers - QB (GB)"
```

## Script Execution

The script includes a main execution block that downloads all players for all sports:

```bash
python download_player_ids.py
```

This will download and print player data for:
- NFL (National Football League)
- MLB (Major League Baseball)
- NBA (National Basketball Association)
- NHL (National Hockey League)

Players are fetched in alphabetical order with a 0.2 second delay between sport requests to avoid rate limiting.
