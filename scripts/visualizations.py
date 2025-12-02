import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.config import DATA_PATHS
import logging

logging.basicConfig(level=logging.INFO)

def run():
    df = pd.read_csv(DATA_PATHS['enriched_reviews'])
    
    # Ratings per bank
    plt.figure(figsize=(8,5))
    sns.boxplot(x='bank', y='rating', data=df)
    plt.title("Ratings Distribution per Bank")
    plt.savefig("reports/ratings_per_bank.png")
    plt.close()

    # Sentiment counts per bank
    plt.figure(figsize=(8,5))
    sns.countplot(x='bank', hue='sentiment_label', data=df)
    plt.title("Sentiment per Bank")
    plt.savefig("reports/sentiments_per_bank.png")
    plt.close()

    # Themes
    themes_expanded = df.explode('themes')
    plt.figure(figsize=(12,6))
    sns.countplot(y='themes', hue='bank', data=themes_expanded)
    plt.title("Themes per Bank")
    plt.savefig("reports/themes_per_bank.png")
    plt.close()

    logging.info("Visualizations saved to reports/")

if __name__=='__main__':
    run()
