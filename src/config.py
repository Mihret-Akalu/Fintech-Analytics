# src/config.py
from pathlib import Path

APP_IDS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "DASHEN": "com.dashen.dashensuperapp"
}

BANK_NAMES = {
    "CBE": "Commercial Bank of Ethiopia",
    "BOA": "Bank of Abyssinia",
    "DASHEN": "Dashen Bank"
}

SCRAPING_CONFIG = {
    "reviews_per_bank": 800,   # try to collect 800 so you can keep >400 after cleaning
    "lang": "en",
    "country": "us",
    "max_retries": 3
}

DATA_PATHS = {
    "raw": str(Path.cwd() / "data"),
    "raw_reviews": str(Path.cwd() / "data" / "reviews_raw.csv"),
    "clean_reviews": str(Path.cwd() / "data" / "reviews_clean.csv"),
    "enriched_reviews": str(Path.cwd() / "data" / "reviews_enriched.csv")
}
