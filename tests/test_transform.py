import unittest

import pandas as pd

from utils.transform import clean_price, clean_rating, clean_colors, clean_field, is_valid_item, remove_duplicates, \
    clean_data, EXCHANGE_RATE_USD_TO_IDR


class TestDataCleaning(unittest.TestCase):

    def test_clean_price(self):
        self.assertEqual(clean_price("$10.00"), 160000)
        self.assertEqual(clean_price("$0.99"), round(0.99 * EXCHANGE_RATE_USD_TO_IDR))

    def test_clean_rating(self):
        self.assertEqual(clean_rating("Rating: ⭐4.5 / 5"), 4.5)
        self.assertEqual(clean_rating("Rating: ⭐3.0 / 5"), 3.0)

    def test_clean_colors(self):
        self.assertEqual(clean_colors("3 Colors"), 3)
        self.assertEqual(clean_colors("10 Colors"), 10)

    def test_clean_field(self):
        self.assertEqual(clean_field("Size: L", "Size:"), "L")
        self.assertEqual(clean_field("Gender: Female", "Gender:"), "Female")

    def test_is_valid_item(self):
        valid_item = {
            "Title": "T-shirt 2",
            "Price": "$20.00",
            "Rating": "Rating: ⭐4.2 / 5",
            "Colors": "5 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Unisex"
        }
        invalid_item_missing = {
            "Title": "Hoodie 3",
            "Price": None,
            "Rating": "Rating: ⭐4.2 / 5",
            "Colors": "5 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Unisex"
        }
        invalid_item_flagged = {
            "Title": "Unknown Product",
            "Price": "$10.00",
            "Rating": "Rating: ⭐4.0 / 5",
            "Colors": "2 Colors",
            "Size": "Size: L",
            "Gender": "Gender: Male"
        }
        self.assertTrue(is_valid_item(valid_item))
        self.assertFalse(is_valid_item(invalid_item_missing))
        self.assertFalse(is_valid_item(invalid_item_flagged))

    def test_remove_duplicates(self):
        items = [
            {"Title": "A", "Price (IDR)": 10000, "Rating": 4.0},
            {"Title": "A", "Price (IDR)": 10000, "Rating": 4.0},
            {"Title": "B", "Price (IDR)": 20000, "Rating": 4.5}
        ]
        result = remove_duplicates(items)
        self.assertEqual(len(result), 2)

    def test_clean_data(self):
        raw_data = [
            {
                "Title": "T-Shirt",
                "Price": "$10.00",
                "Rating": "Rating: ⭐4.0 / 5",
                "Colors": "3 Colors",
                "Size": "Size: M",
                "Gender": "Gender: Male",
                "Timestamp": "2025-01-01T10:00:00"
            },
            {
                "Title": "T-Shirt",
                "Price": "$10.00",
                "Rating": "Rating: ⭐4.0 / 5",
                "Colors": "3 Colors",
                "Size": "Size: M",
                "Gender": "Gender: Male",
                "Timestamp": "2025-01-01T10:00:00"
            },
            {
                "Title": "Unknown Product",
                "Price": "$5.00",
                "Rating": "Rating: ⭐3.0 / 5",
                "Colors": "2 Colors",
                "Size": "Size: S",
                "Gender": "Gender: Female"
            }
        ]

        cleaned = clean_data(raw_data)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned[0]["Title"], "T-Shirt")
        self.assertEqual(cleaned[0]["Price (IDR)"], 160000)
        self.assertEqual(cleaned[0]["Rating"], 4.0)
        self.assertEqual(cleaned[0]["Colors"], 3)
        self.assertEqual(cleaned[0]["Size"], "M")
        self.assertEqual(cleaned[0]["Gender"], "Male")

    def test_convert_dtypes(self):
        df = pd.DataFrame({
            "Title": ["T-Shirt 2"],
            "Price (IDR)": [160000],
            "Rating": [4.5],
            "Colors": [3],
            "Size": ["M"],
            "Gender": ["Unisex"],
            "Timestamp": ["2025-01-01T10:00:00"]
        })

        from utils.transform import convert_dtypes
        converted_df = convert_dtypes(df)

        self.assertEqual(converted_df["Price (IDR)"].dtype, "float64")
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(converted_df["Timestamp"]))


if __name__ == "__main__":
    unittest.main()
