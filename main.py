import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

game_id = "0022301057"
season = "2023-24"
url = f"https://www.nba.com/game/hou-vs-okc-{game_id}/play-by-play?period=All"

response = requests.get(url)

if response.status_code == 200:
  text = response.text
  pattern = r'{"actionNumber":\d+.*?\}'
  matches = re.findall(pattern, text)

  free_throws = []

  for match in matches:
    try:
      obj = json.loads(match)
      if obj.get("actionType") == "Free Throw":
        free_throws.append(obj)
    except json.JSONDecodeError:
      continue

  print(f"Found {len(free_throws)} free throw actions:\n")
  output_dir = os.path.join(os.getcwd(), game_id)
  os.makedirs(output_dir, exist_ok=True)

  options = webdriver.ChromeOptions()
  driver = webdriver.Chrome(options=options)

  for action in free_throws:
    # print(json.dumps(action, indent=2))

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
    
    try:
      driver.get(url)

      # Wait up to 15 seconds for the video element to appear
      video_element = WebDriverWait(driver, 15).until(
          EC.presence_of_element_located((By.TAG_NAME, "video"))
      )

      video_url = video_element.get_attribute("src")
      print("✅ Found video URL:", video_url)
      
      r = requests.get(video_url)
      with open(os.path.join(output_dir, f"{action['actionNumber']}.mp4"), "wb") as f:
          f.write(r.content)

    except Exception as e:
      print("❌ Error:", e)
      print("URL:", url)
      print("Action:", json.dumps(action, indent=2))
      continue

  driver.quit()
  print(f"Videos saved in {output_dir}")
  
else:
  print("Failed to load page")
  print("Status code:", response.status_code)
  print("Response text:", response.text)
  exit()