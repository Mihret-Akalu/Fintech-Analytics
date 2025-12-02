import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from src.config import DATA_PATHS

# PostgreSQL connection details
DB_HOST = 'localhost'
DB_NAME = 'bank_reviews'
DB_USER = 'postgres'
DB_PASSWORD = '1627'  # replace with your PostgreSQL password
DB_PORT = 5432  # default port

def run():
    # Load cleaned reviews
    df = pd.read_csv(DATA_PATHS['enriched_reviews'])

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # Insert banks
    banks = df[['bank', 'app_id']].drop_duplicates()
    bank_tuples = list(banks.itertuples(index=False, name=None))
    insert_banks_query = """
        INSERT INTO banks (bank_name, app_id)
        VALUES %s
        ON CONFLICT (app_id) DO NOTHING;
    """
    execute_values(cursor, insert_banks_query, bank_tuples)

    # Map bank_name -> bank_id
    cursor.execute("SELECT bank_id, bank_name FROM banks;")
    bank_map = {name: id for id, name in cursor.fetchall()}

    # Insert reviews
    review_tuples = []
    for _, row in df.iterrows():
        review_tuples.append((
            bank_map[row['bank']], 
            row['review'], 
            int(row['rating']), 
            row['date'], 
            row.get('sentiment_label', None),
            row.get('sentiment_score', None),
            str(row.get('themes', None)),
            row.get('source', 'Google Play')
        ))

    insert_reviews_query = """
        INSERT INTO reviews 
        (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, themes, source)
        VALUES %s;
    """
    execute_values(cursor, insert_reviews_query, review_tuples)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted {len(df)} reviews into PostgreSQL.")

if __name__ == "__main__":
    run()
