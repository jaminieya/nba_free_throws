import urllib.parse

# Builds a URL for the NBA stats event page based on the action details. 
def build_stats_event_url(action: dict, game_id: str, season: str) -> str:
  title_encoded = urllib.parse.quote(action["description"])
  url = (
      f"https://www.nba.com/stats/events?"
      f"CFID=&CFPARAMS=&"
      f"GameEventID={action['actionNumber']}&"
      f"GameID={game_id}&"
      f"Season={season}&"
      f"flag=1&"
      f"title={title_encoded}"
  )
  return url