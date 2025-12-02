import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

df = pd.read_csv("data/processed/cleaned_reviews.csv")

sid = SentimentIntensityAnalyzer()
df['sentiment_score'] = df['review_text'].apply(lambda x: sid.polarity_scores(str(x))['compound'])
df['sentiment_label'] = df['sentiment_score'].apply(lambda x: 'Positive' if x>0 else ('Negative' if x<0 else 'Neutral'))

df.to_csv("data/processed/enriched_reviews.csv", index=False)
print("Sentiment analysis complete")
