import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from src.config import DATA_PATHS
import os
import logging

logging.basicConfig(level=logging.INFO)

REPORT_PATH = "reports/final_report.pdf"
PLOTS_DIR = "reports/"

# Ensure reports folder exists
os.makedirs(PLOTS_DIR, exist_ok=True)

def save_plots(df):
    # Ratings distribution per bank
    plt.figure(figsize=(8,5))
    sns.boxplot(x='bank', y='rating', data=df)
    plt.title("Ratings Distribution per Bank")
    rating_path = os.path.join(PLOTS_DIR, "ratings_per_bank.png")
    plt.savefig(rating_path)
    plt.close()

    # Sentiment counts per bank
    plt.figure(figsize=(8,5))
    sns.countplot(x='bank', hue='sentiment_label', data=df)
    plt.title("Sentiment per Bank")
    sentiment_path = os.path.join(PLOTS_DIR, "sentiments_per_bank.png")
    plt.savefig(sentiment_path)
    plt.close()

    # Themes per bank
    themes_expanded = df.explode('themes')
    plt.figure(figsize=(12,6))
    sns.countplot(y='themes', hue='bank', data=themes_expanded)
    plt.title("Themes per Bank")
    themes_path = os.path.join(PLOTS_DIR, "themes_per_bank.png")
    plt.savefig(themes_path)
    plt.close()

    logging.info("Plots saved.")
    return rating_path, sentiment_path, themes_path

def generate_insights(df):
    insights = []
    banks = df['bank'].unique()
    for bank in banks:
        sub = df[df['bank'] == bank]
        # Drivers
        top_pos = sub[sub['sentiment_label']=='positive']['themes'].explode().value_counts().head(2).index.tolist()
        # Pain points
        top_neg = sub[sub['sentiment_label']=='negative']['themes'].explode().value_counts().head(2).index.tolist()
        # Recommendations (generic examples, can refine)
        recs = [
            f"Enhance {top_neg[0]} experience" if top_neg else "Monitor performance",
            f"Improve {top_neg[1]}" if len(top_neg)>1 else "Focus on customer support"
        ]
        insights.append({
            "bank": bank,
            "top_drivers": ", ".join(top_pos) if top_pos else "None",
            "top_pain_points": ", ".join(top_neg) if top_neg else "None",
            "recommendations": "; ".join(recs)
        })
    return insights

def build_pdf(df):
    rating_path, sentiment_path, themes_path = save_plots(df)
    insights = generate_insights(df)

    doc = SimpleDocTemplate(REPORT_PATH, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Bank App Reviews Analysis", styles['Title']))
    story.append(Spacer(1,12))

    # Add plots
    for path, title in zip([rating_path, sentiment_path, themes_path],
                           ["Ratings per Bank", "Sentiments per Bank", "Themes per Bank"]):
        story.append(Paragraph(title, styles['Heading2']))
        story.append(Image(path, width=400, height=250))
        story.append(Spacer(1,12))

    # Add insights
    story.append(Paragraph("Insights & Recommendations per Bank", styles['Heading2']))
    for i in insights:
        text = f"<b>{i['bank']}</b><br/>Top Drivers: {i['top_drivers']}<br/>" \
               f"Pain Points: {i['top_pain_points']}<br/>" \
               f"Recommendations: {i['recommendations']}<br/><br/>"
        story.append(Paragraph(text, styles['BodyText']))

    doc.build(story)
    logging.info(f"PDF report generated at {REPORT_PATH}")

def run():
    if not os.path.exists(DATA_PATHS['enriched_reviews']):
        logging.error(f"Enriched CSV not found at {DATA_PATHS['enriched_reviews']}")
        return
    df = pd.read_csv(DATA_PATHS['enriched_reviews'])
    # Ensure themes column is list
    if df['themes'].dtype == 'O':
        df['themes'] = df['themes'].apply(lambda x: eval(x) if isinstance(x,str) else [])
    build_pdf(df)

if __name__=="__main__":
    run()
