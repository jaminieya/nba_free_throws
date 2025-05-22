import argparse
import re
import sys

# Parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="NBA Free Throw Video Scraper")

    # Add arguments
    parser.add_argument("--game_id", type=str, help="Game ID (e.g. 0042400301)")
    parser.add_argument("--url", type=str, help="Full NBA.com play-by-play URL")

    args = parser.parse_args()

    # Input validation
    if args.url:
        # Try to extract game_id from the URL
        match = re.search(r"/game/([a-z]+-vs-[a-z]+)-(\d{10})(?:/|$)", args.url)
        if not match:
            print("❌ Invalid URL format. Example: https://www.nba.com/game/ind-vs-nyk-0042400301/play-by-play")
            sys.exit(1)
        game_id = match.group(2)
    elif args.game_id:
        # Use provided game_id and game_code
        game_id = args.game_id
    else:
        # No valid input provided
        print("❌ You must either provide --url or both --game_id and --game_code.")
        parser.print_help()
        sys.exit(1)

    return game_id
