import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import APP_IDS, BANK_NAMES, SCRAPING_CONFIG, DATA_PATHS
import pandas as pd
from google_play_scraper import reviews, Sort
from datetime import datetime
import time

def scrape_reviews(app_id, count=400):
    for attempt in range(SCRAPING_CONFIG['max_retries']):
        try:
            result, _ = reviews(
                app_id,
                lang=SCRAPING_CONFIG['lang'],
                country=SCRAPING_CONFIG['country'],
                sort=Sort.NEWEST,
                count=count
            )
            return result
        except Exception as e:
            if attempt < SCRAPING_CONFIG['max_retries'] - 1:
                time.sleep(5)
            else:
                return []

def process_reviews(raw_reviews, bank_code):
    processed = []
    for r in raw_reviews:
        processed.append({
            "review": r.get("content", ""),
            "rating": r.get("score", 0),
            "date": r.get("at"),
            "bank": BANK_NAMES[bank_code],
            "bank_code": bank_code,
            "app_id": r.get("reviewCreatedVersion", "N/A"),
            "source": "Google Play"
        })
    return processed

def main():
    all_reviews = []
    for bank_code, app_id in APP_IDS.items():
        raw = scrape_reviews(app_id, SCRAPING_CONFIG['reviews_per_bank'])
        processed = process_reviews(raw, bank_code)
        all_reviews.extend(processed)

    df = pd.DataFrame(all_reviews)
    os.makedirs(os.path.dirname(DATA_PATHS['raw_reviews']), exist_ok=True)
    df.to_csv(DATA_PATHS['raw_reviews'], index=False)
    print("Saved raw reviews:", DATA_PATHS['raw_reviews'])

if __name__ == "__main__":
    main()
