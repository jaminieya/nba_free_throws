# 🏀 NBA Free Throw Video Scraper

A command-line utility that scrapes **Free Throw** events from any NBA game, downloads the associated play-by-play videos from NBA.com, and stores rich metadata for each clip.

---

## 📌 Key Features

* **Flexible CLI** – run the scraper with
  *either* `--url` **or** the pair `--game_id` + `--game_code` (optionally `--season`).
* **Play-by-play parsing** – pulls live play data and filters for `"Free Throw"` actions only.
* **Modular design** – core logic lives in reusable helpers inside **`utils/`**.
* **Dynamic video capture** – Selenium renders the event page and extracts the hidden `<video>` source.
* **Automatic organisation** – videos saved as `<personId>_Shot_<runningNumber>.mp4` inside a folder named after the game ID; a `metadata.csv` file summarises every clip.

---

## 🗂️ Project Structure

```text
nba-free-throw-scraper/
├── main.py                  # CLI entry-point
├── requirements.txt         # Python deps
├── README.md
├── utils/
│   ├── __init__.py
│   ├── shots.py             # shot_number_up_to_event()
│   ├── url_builder.py       # build_stats_event_url()
│   └── video_downloader.py  # download_video_from_event_page()
└── <GAME_ID>/               # Auto-created on run (e.g. 0022301057/)
    ├── metadata.csv         # Metadata for every free-throw
    ├── 763.mp4              # One clip per event
    └── ...
```

---

## 🚀 Quick Start

### 1. Clone & enter the repo

```bash
git clone https://github.com/jaminieya/nba_free_throw_scraper.git
cd nba_free_throw_scraper
```

### 2. Install dependencies

```bash
python -m venv .venv && source .venv/bin/activate   # optional but recommended
pip install -r requirements.txt
```

> **Python 3.8+** is recommended.

### 3. Install ChromeDriver

1. Check your local Chrome version (⋮ → **Help → About Google Chrome**).
2. Download the matching driver from the [official site](https://sites.google.com/chromium.org/driver/).
3. Place `chromedriver` in your **PATH** (or update `video_downloader.py` with the driver path).

### 4. Run the scraper

#### Option A — Game ID + Code

```bash
python main.py \
  --game_id 0042400301 \
  --game_code ind-vs-nyk \
  --season 2024-25          # optional; defaults to 2023-24
```

#### Option B — Full URL

*(remember to quote the URL in zsh/Bash!)*

```bash
python main.py \
  --url "https://www.nba.com/game/ind-vs-nyk-0042400301/play-by-play?period=All"
```

### 5. Output

* A folder named after `game_id` appears in the project root.
* Inside you’ll find an MP4 for every free-throw and a `metadata.csv` with

  | Column        | Description                           |
  | ------------- | ------------------------------------- |
  | `Video Name`  | `<personId>_Shot_<runningNumber>.mp4` |
  | `link`        | Stats event page                      |
  | `teams`       | Concatenated tricode (e.g. `INDNYK`)  |
  | `game_id`     | NBA Game ID                           |
  | `player_name` | Full player name                      |
  | `player_id`   | NBA player ID                         |
  | `player_team` | Player’s team tricode                 |
  | `make/miss`   | `"MAKE"` / `"MISS"` flag              |

---

## 🧰 Dependency List

```
beautifulsoup4
numpy
pandas
nba_api
requests
selenium
```

All dependencies are pinned in **requirements.txt**.

---

## ⚠️ Notes & Disclaimer

* This script is intended **for educational / personal use only**.
* Always review and respect the [NBA Terms of Use](https://www.nba.com/termsofuse) when downloading content.
* Website structures can change; if scraping fails, update the selectors or check for an official API endpoint.

---

## 🙌 Acknowledgements

* **NBA.com** for providing public play-by-play data and video highlights.
* The communities behind **Selenium**, **BeautifulSoup**, and **nba\_api** for their excellent open-source tools.
