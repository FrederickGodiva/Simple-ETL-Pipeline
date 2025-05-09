import os

import pandas as pd
from dotenv import load_dotenv

from utils.extract import scrape
from utils.load import save_to_csv, save_to_google_sheets, load_to_postgresql
from utils.transform import clean_data, convert_dtypes

load_dotenv()

BASE_URL = "https://fashion-studio.dicoding.dev/"
MAX_PAGES = 50

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_RANGE = "Sheet1!A1"


def main():
    print("[INFO] Starting ETL pipeline...")

    # Extract
    raw_data = scrape(BASE_URL, max_pages=MAX_PAGES, delay=1)

    if not raw_data:
        print("[WARN] No data scraped. Exiting.")
        return

    # Transform
    data = clean_data(raw_data)
    cleaned_data = pd.DataFrame(data)
    df = convert_dtypes(cleaned_data)

    if df.empty:
        print("[WARN] Cleaned data is empty. Exiting.")
        return

    # Load
    save_to_csv(df, filename="fashion_products.csv")
    save_to_google_sheets(df, SPREADSHEET_ID, SHEET_RANGE)
    load_to_postgresql(df, "fashion_products")

    print("[INFO] ETL pipeline completed successfully.")


if __name__ == "__main__":
    main()
