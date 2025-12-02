# scripts/visualizations.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from ast import literal_eval
from src.config import DATA_PATHS

sns.set(style="whitegrid")

def plot_rating_distribution(df):
    """Plot rating distribution per bank"""
    for bank in df['bank'].unique():
        sub = df[df['bank'] == bank]
        plt.figure(figsize=(6,4))
        sns.countplot(x='rating', data=sub, palette="viridis")
        plt.title(f"{bank} - Rating Distribution")
        plt.xlabel("Rating")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

def plot_sentiment_distribution(df):
    """Plot sentiment label distribution per bank"""
    for bank in df['bank'].unique():
        sub = df[df['bank'] == bank]
        plt.figure(figsize=(6,4))
        sns.countplot(x='sentiment_label', data=sub, palette="Set2",
                      order=['positive', 'neutral', 'negative'])
        plt.title(f"{bank} - Sentiment Distribution")
        plt.xlabel("Sentiment")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

def plot_theme_counts(df):
    """Plot theme counts per bank"""
    for bank in df['bank'].unique():
        sub = df[df['bank'] == bank]
        # Convert string representation of list to actual list
        themes_lists = sub['themes'].apply(lambda x: literal_eval(x) if isinstance(x, str) else x)
        # Flatten list of themes
        all_themes = [t for sublist in themes_lists for t in sublist]
        counts = Counter(all_themes)
        plt.figure(figsize=(8,4))
        sns.barplot(x=list(counts.keys()), y=list(counts.values()), palette="coolwarm")
        plt.title(f"{bank} - Themes Frequency")
        plt.xticks(rotation=45, ha='right')
        plt.xlabel("Theme")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

def run():
    print("Loading enriched reviews...")
    df = pd.read_csv(DATA_PATHS['enriched_reviews'])
    
    print("Plotting rating distributions...")
    plot_rating_distribution(df)

    print("Plotting sentiment distributions...")
    plot_sentiment_distribution(df)

    print("Plotting theme frequencies...")
    plot_theme_counts(df)

    print("All plots generated successfully!")

if __name__ == "__main__":
    run()
