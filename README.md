```markdown
# 🏀 NBA Free Throw Video Scraper

This project scrapes **Free Throw** events from an NBA game and downloads their associated videos from the NBA.com stats website.

## 📌 Features

- Scrapes play-by-play data for a specific NBA game.
- Filters for events of type `"Free Throw"`.
- Builds video URLs using NBA's stats event viewer.
- Uses Selenium to extract dynamically loaded video sources.
- Downloads and saves videos in a folder named after the game ID.

## 📂 Folder Structure


main.py
requirements.txt
0022301057/                  # Automatically created
├── 763.mp4
├── 764.mp4
└── ...

## 🚀 How to Run

### 1. Clone this repository

git clone https://github.com/jaminieya/nba_free_throws.git
cd nba_free_throws


### 2. Install dependencies

Make sure you have Python 3.8+ installed. Then run:

pip install -r requirements.txt


### 3. Install ChromeDriver

* Download [ChromeDriver](https://sites.google.com/chromium.org/driver/) that matches your Chrome version.
* Place it in your system PATH or specify its location in the script if needed.

### 4. Run the scraper

python main.py

By default, the script scrapes game ID `0022301057` and saves videos into a folder named `0022301057/`.

## 🧰 Dependencies

* `requests`
* `beautifulsoup4`
* `selenium`

All dependencies are listed in `requirements.txt`.

## 📌 Notes

* This script is designed for educational use.
* Make sure your usage complies with the [NBA's Terms of Use](https://www.nba.com/termsofuse).

---

## 🙌 Acknowledgments

* NBA.com for providing detailed game data and videos.
* `selenium` and `BeautifulSoup` open-source communities.

````

