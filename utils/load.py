import os

import pandas as pd
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

load_dotenv()

SERVICE_ACCOUNT_FILE = './client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

DB_CONFIG = {
    'username': os.getenv("DB_USERNAME"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
    'database': os.getenv("DB_NAME")
}


def save_to_csv(df, filename):
    """
    Saves a pandas DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        filename (str): The name of the CSV file to write to.

    Returns:
        None
    """
    df.to_csv(filename, index=False)
    print(f"Data successfully saved to {filename}.")


def save_to_google_sheets(df, spreadsheet_id, range_name):
    """
    Uploads a pandas DataFrame to a specific range in a Google Sheets spreadsheet.

    Args:
        df (pd.DataFrame): The DataFrame to upload.
        spreadsheet_id (str): The ID of the target Google Sheets document.
        range_name (str): The A1 notation of the range to populate (e.g., "Sheet1!A1").

    Returns:
        None
    """
    df["Timestamp"] = df["Timestamp"].astype(str)
    try:
        credential = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE).with_scopes(SCOPES)
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()

        # Convert the DataFrame to a list of lists, including headers
        values = [df.columns.tolist()] + df.values.tolist()
        body = {'values': values}

        # Upload data to Google Sheets
        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"Data successfully saved to Google Sheets in range '{range_name}'.")

    except Exception as e:
        print(f"[ERROR] Failed to save to Google Sheets: {e}")


def load_to_postgresql(df, table_name):
    """
    Loads a pandas DataFrame into a PostgreSQL database table.

    Args:
        df (pd.DataFrame): The DataFrame to store.
        table_name (str): The name of the target table in the database.

    Returns:
        None
    """
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DB_CONFIG['username']}:{DB_CONFIG['password']}"
            f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )

        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data successfully saved to PostgreSQL table '{table_name}'.")

    except Exception as e:
        print(f"[ERROR] Failed to save to PostgreSQL: {e}")
