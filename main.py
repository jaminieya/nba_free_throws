import os
import re
import csv
import sys
import json
import argparse
import requests
import urllib.parse
import pandas as pd
import numpy as np
from utils.shots import shot_number_up_to_event
from utils.url_builder import build_stats_event_url
from utils.video_downloader import download_video_from_event_page
from utils.parse import parse_args
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nba_api.stats.static import players
from nba_api.stats.endpoints import PlayByPlayV2, BoxScoreSummaryV2

# NBA Free Throw Video Downloader
# This script downloads free throw videos from NBA games and saves them in a specified folder.
# It also generates a metadata CSV file with information about each video.

# Configuration
game_id = parse_args()
summary = BoxScoreSummaryV2(game_id=game_id).get_normalized_dict()
home_team = summary["GameSummary"][0]["GAMECODE"][-6:-3]
away_team = summary["GameSummary"][0]["GAMECODE"][-3:]
game_code = f"{home_team.lower()}-vs-{away_team.lower()}"
teams = f"{home_team}{away_team}"
season = summary["GameSummary"][0]["SEASON"]
url = f"https://www.nba.com/game/{game_code}-{game_id}/play-by-play?period=All"

# 1. Load the game page
response = requests.get(url)

if response.status_code != 200:
  print("Failed to load page")
  print("Status code:", response.status_code)
  exit()

# 2. Extract all action JSON objects
pattern = r'{"actionNumber":\d+.*?\}'
matches = re.findall(pattern, response.text)

free_throws = []
metadata_rows = []

# 2-1. Filter for free throw actions
for match in matches:
  try:
    obj = json.loads(match)
    if obj.get("actionType") == "Free Throw":
      free_throws.append(obj)
  except json.JSONDecodeError:
    continue

# 3. Prepare output folder
print(f"Found {len(free_throws)} free throw actions:\n")
output_dir = os.path.join(os.getcwd(), game_id)
os.makedirs(output_dir, exist_ok=True)

# 4. Setup Selenium WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)


# 5. Loop through free throw actions and download videos
for action in free_throws:

  # Storing metadata
  url = build_stats_event_url(action, game_id, season)
  shot_attempts = shot_number_up_to_event(game_id, action["personId"], action["actionNumber"])
  vid_name = f"{action['personId']}_Shot_{shot_attempts}"

  metadata_rows.append({
    "Video Name": vid_name,
    "link": url,
    "teams": teams,
    "game_id": game_id,
    "player_name": players.find_player_by_id(action["personId"])["full_name"],
    "player_id": action["personId"],
    "player_team": action["teamTricode"],
    "make/miss": "MISS" if action["description"].startswith("MISS") else "MAKE",
  })

  # Download video
  save_path = os.path.join(output_dir, f"{vid_name}.mp4")
  success = download_video_from_event_page(driver, url, save_path)
  if not success:
    continue

driver.quit()

# 6. Save metadata to CSV
csv_path = os.path.join(output_dir, "metadata.csv")
with open(csv_path, "w", newline="") as csvfile:
  fieldnames = metadata_rows[0].keys()
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
  for row in metadata_rows:
    writer.writerow(row)

# 7. Done
print(f"Videos saved in {output_dir}")
print(f"Metadata saved to {csv_path}")
