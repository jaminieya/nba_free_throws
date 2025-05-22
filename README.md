# 🏀 NBA Free Throw Video Scraper

A command‑line utility that scrapes **Free Throw** events from any NBA game, downloads the associated play‑by‑play videos from NBA.com, and stores rich metadata for each clip.

---

## 📌 Key Features

* **CLI interface** – run the scraper from the terminal with `--game_id`, `--game_code`, and `--season` arguments.
* **Play‑by‑play parsing** – pulls live play data, filters for `"Free Throw"` actions.
* **Modular design** – core logic is split into reusable helpers inside `utils/`.
* **Dynamic video capture** – Selenium renders the event page and extracts the hidden `<video>` source.
* **Automatic organisation** – videos saved as `<personId>_Shot_<runningNumber>.mp4` inside a folder named after the game ID; a `metadata.csv` file summarises every clip.

---

## 🗂️ Project Structure

```text
nba-free-throw-scraper/
├── main.py                  # CLI entry‑point
├── requirements.txt         # Python deps
├── README.md
├── utils/
│   ├── __init__.py          # Package marker
│   ├── shots.py             # shot_number_up_to_event()
│   ├── url_builder.py       # build_stats_event_url()
│   └── video_downloader.py  # download_video_from_event_page()
└── <GAME_ID>/               # Auto‑created on run (e.g. 0022301057/)
    ├── metadata.csv         # Metadata for every free‑throw
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

> **Python 3.8+** is recommended.

### 3. Install ChromeDriver

1. Check your local Chrome version (⋮ → **Help → About Google Chrome**).
2. Download the matching driver from the [official site](https://sites.google.com/chromium.org/driver/).
3. Place `chromedriver` in your **PATH** or pass `options.binary_location`/`service=Service('path')` in `video_downloader.py`.

### 4. Run the scraper

```bash
python main.py \
  --game_id 0022301057 \
  --game_code hou-vs-okc \
  --season 2023-24
```

*All arguments are **required**.*

### 5. Output

* A folder named after `--game_id` will appear in the project root.
* Inside you’ll find an MP4 for every free‑throw and a `metadata.csv` with:

  * video filename
  * link to the stats event page
  * teams in the game (e.g. `HOUOKC`)
  * player name & ID
  * make/miss flag

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
* Website structures can change; if scraping fails, update the CSS selectors or check for an official API endpoint.

---

## 🙌 Acknowledgements

* **NBA.com** for providing public play‑by‑play data and video highlights.
* The communities behind **Selenium**, **BeautifulSoup**, and **nba\_api** for their excellent open‑source tools.
