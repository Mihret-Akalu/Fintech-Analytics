import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATHS = {
    "raw_reviews": os.path.join(PROJECT_ROOT, "data/raw/raw_reviews.csv"),
    "clean_reviews": os.path.join(PROJECT_ROOT, "data/processed/cleaned_reviews.csv"),
    "enriched_reviews": os.path.join(PROJECT_ROOT, "data/processed/enriched_reviews.csv")
}

APP_IDS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp"
}

BANK_NAMES = {
    "CBE": "Commercial Bank of Ethiopia",
    "BOA": "Bank of Abyssinia",
    "Dashen": "Dashen Bank"
}

SCRAPING_CONFIG = {
    "reviews_per_bank": 400,
    "lang": "en",
    "country": "us",
    "max_retries": 3
}
