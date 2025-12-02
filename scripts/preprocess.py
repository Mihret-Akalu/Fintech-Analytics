import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from dateutil import parser
from src.config import DATA_PATHS

def normalize_date(d):
    if pd.isna(d):
        return None
    try:
        return parser.parse(str(d)).date().isoformat()
    except Exception:
        return None

def main():
    df = pd.read_csv(DATA_PATHS['raw_reviews'])
    df.rename(columns={"review_text":"review","review_date":"date","bank_name":"bank"}, inplace=True)
    df = df.dropna(subset=['review','rating'])
    df['review'] = df['review'].astype(str).str.strip()
    df = df[df['review'].str.len() > 0]
    df['date'] = df['date'].apply(normalize_date)
    df = df.drop_duplicates(subset=['review','bank'])
    out = df[['review','rating','date','bank','bank_code','app_id','source']]
    os.makedirs(os.path.dirname(DATA_PATHS['clean_reviews']), exist_ok=True)
    out.to_csv(DATA_PATHS['clean_reviews'], index=False)
    print("Saved cleaned reviews:", DATA_PATHS['clean_reviews'])
    print("Total rows:", len(out))

if __name__ == "__main__":
    main()
