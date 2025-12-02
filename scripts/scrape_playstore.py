"""
scrape_playstore.py

Scrapes reviews from selected Ethiopian banking apps on Google Play Store
and saves them as a CSV file in data/raw/.

Requires:
    pip install google-play-scraper pandas

Folder structure:
    fintech-analytics/
        data/
            raw/
            processed/
        scripts/
            scrape_playstore.py
"""
from google_play_scraper import reviews, Sort
import pandas as pd
import os
import datetime


# -------------------------------------------------------------------
# 1. Configure the apps to scrape (package names from Google Play)
# -------------------------------------------------------------------
BANK_APPS = {
   "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "DASHEN": "com.dashen.dashensuperapp"
}


# -------------------------------------------------------------------
# 2. Scrape function
# -------------------------------------------------------------------
def scrape_app_reviews(app_name: str, package_name: str, n=200):
    """
    Scrapes the latest n Google Play reviews for a given app.
    Returns a dataframe with cleaned review data.
    """

    print(f"\n📥 Scraping {n} reviews for: {app_name}...")

    result, _ = reviews(
        package_name,
        lang="en",
        country="us",
        sort=Sort.NEWEST,
        count=n
    )

    df = pd.DataFrame(result)

    if df.empty:
        print(f"⚠ No reviews found for {app_name}.")
        return df

    # Clean the dataframe
    df = df[["content", "score", "reviewCreatedVersion", "at"]]
    df.rename(columns={
        "content": "review",
        "score": "rating",
        "reviewCreatedVersion": "version",
        "at": "date"
    }, inplace=True)

    df["bank_name"] = app_name
    df["source"] = "Google Play Store"

    return df


# -------------------------------------------------------------------
# 3. Main script logic
# -------------------------------------------------------------------
def main():
    all_reviews = []

    for bank, pkg in BANK_APPS.items():
        df = scrape_app_reviews(bank, pkg, n=150)

        if not df.empty:
            all_reviews.append(df)

    if not all_reviews:
        print("\n❌ No data scraped. Exiting.")
        return

    final_df = pd.concat(all_reviews, ignore_index=True)

    print("\n📊 Total reviews scraped:", len(final_df))

    # Ensure output directory exists
    output_dir = os.path.join("data", "raw")
    os.makedirs(output_dir, exist_ok=True)

    # Save with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    output_path = os.path.join(output_dir, f"playstore_reviews_{timestamp}.csv")

    final_df.to_csv(output_path, index=False)

    print(f"\n✅ Saved scraped data to:\n   {output_path}")


# -------------------------------------------------------------------
# Run the script
# -------------------------------------------------------------------
if __name__ == "__main__":
    main()
