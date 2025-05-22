import os
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Builds a URL for video page based on the action details.
def download_video_from_event_page(driver, url: str, save_path: str) -> bool:
    """
    Visit the stats event page using selenium, extract video URL,
    and download the video to save_path. Returns True if successful.
    """
    try:
      # Visit the NBA stats event page
      driver.get(url)

      # Wait up to 15 seconds for the video element to appear
      video_element = WebDriverWait(driver, 15).until(
          EC.presence_of_element_located((By.TAG_NAME, "video"))
      )

      # Extract the video URL from the video element
      video_url = video_element.get_attribute("src")
      print("✅ Found video URL:", video_url)
      
      # Download the video
      video_data = requests.get(video_url)
      with open(save_path, "wb") as f:
          f.write(video_data.content)
      return True
    
    except Exception as e:
      print("❌ Error:", e)
      print("URL:", url)
      return False
