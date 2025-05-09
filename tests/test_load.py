import unittest
from unittest.mock import patch, MagicMock

import pandas as pd

from utils.load import save_to_csv, save_to_google_sheets, load_to_postgresql


class TestLoadFunctions(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'Name': ['Alice', 'Bob'],
            'Age': [30, 25],
            'Timestamp': ['2024-01-01', '2024-01-02']
        })

    @patch("pandas.DataFrame.to_csv")
    def test_save_to_csv(self, mock_to_csv):
        save_to_csv(self.df, "test.csv")
        mock_to_csv.assert_called_once_with("test.csv", index=False)

    @patch("utils.load.Credentials.from_service_account_file")
    @patch("utils.load.build")
    def test_save_to_google_sheets(self, mock_build, mock_credentials):
        mock_service = MagicMock()
        mock_sheet = mock_service.spreadsheets.return_value
        mock_values = mock_sheet.values.return_value
        mock_values.update.return_value.execute.return_value = None

        mock_credentials.return_value.with_scopes.return_value = MagicMock()
        mock_build.return_value = mock_service

        spreadsheet_id = "dummy_spreadsheet_id"
        range_name = "Sheet1!A1"

        save_to_google_sheets(self.df, spreadsheet_id, range_name)

        mock_build.assert_called_once_with('sheets', 'v4',
                                           credentials=mock_credentials.return_value.with_scopes.return_value)
        mock_values.update.assert_called_once()

    @patch("utils.load.create_engine")
    @patch("pandas.DataFrame.to_sql")
    def test_load_to_postgresql(self, mock_to_sql, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        load_to_postgresql(self.df, "people")

        mock_create_engine.assert_called_once()
        mock_to_sql.assert_called_once_with("people", mock_engine, if_exists='replace', index=False)


if __name__ == "__main__":
    unittest.main()
