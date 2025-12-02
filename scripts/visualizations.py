# scripts/visualizations.py
import pandas as pd
import matplotlib.pyplot as plt
from src.config import DATA_PATHS

def run():
    df = pd.read_csv(DATA_PATHS['enriched_reviews'])
    # Example: Rating distribution per bank
    for bank in df['bank'].unique():
        sub = df[df['bank'] == bank]
        sub['rating'].value_counts().sort_index().plot(kind='bar', title=f"{bank} Rating Distribution")
        plt.xlabel("Rating")
        plt.ylabel("Count")
        plt.show()

if __name__ == "__main__":
    run()
