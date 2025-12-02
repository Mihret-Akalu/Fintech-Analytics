import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from src.config import DATA_PATHS
import spacy
nlp = spacy.load('en_core_web_sm')

THEME_MAP = {
    "Account Access": ["login","password","otp","pin","biometric","fingerprint","access"],
    "Transaction Performance": ["slow","loading","timeout","transfer","transaction","processing","pending"],
    "Stability & Bugs": ["crash","error","failed","bug","freeze","hang"],
    "UI & UX": ["ui","interface","design","navigate","easy","confusing","layout"],
    "Customer Support": ["support","help","service","call","response","agent"],
    "Feature Requests": ["feature","fingerprint","statement","history","notifications","limit"]
}

def preprocess(text):
    doc = nlp(str(text).lower())
    tokens = [t.lemma_ for t in doc if t.is_alpha and not t.is_stop and len(t)>2]
    return " ".join(tokens)

def assign_themes(text):
    t = str(text).lower()
    hits=[]
    for theme, kws in THEME_MAP.items():
        for kw in kws:
            if kw in t:
                hits.append(theme)
                break
    return hits if hits else ["Other"]

def main():
    df = pd.read_csv(DATA_PATHS['enriched_reviews'])
    df['themes'] = df['review'].map(assign_themes)
    df.to_csv(DATA_PATHS['enriched_reviews'], index=False)
    print("Themes assigned and saved:", DATA_PATHS['enriched_reviews'])

if __name__=="__main__":
    main()
