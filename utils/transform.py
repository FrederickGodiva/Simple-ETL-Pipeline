import pandas as pd

EXCHANGE_RATE_USD_TO_IDR = 16000


def clean_price(price_str):
    """
    Converts a price string in USD to an integer in IDR.

    Args:
        price_str (str): A price string like "$19.99".

    Returns:
        int: The price in Indonesian Rupiah (IDR).
    """
    return round(float(price_str.replace("$", "").strip()) * EXCHANGE_RATE_USD_TO_IDR)


def clean_rating(rating_str):
    """
    Extracts the numerical rating from a formatted string.

    Args:
        rating_str (str): A rating string like "Rating: ⭐4.5 / 5".

    Returns:
        float: The numerical rating (e.g., 4.5).
    """
    return float(rating_str.replace("Rating: ⭐", "").replace("/ 5", "").strip())


def clean_colors(colors_str):
    """
    Extracts the number of colors from a formatted string.

    Args:
        colors_str (str): A string like "5 Colors".

    Returns:
        int: The number of colors (e.g., 5).
    """
    return int(colors_str.replace("Colors", "").strip())


def clean_field(field_str, prefix):
    """
    Removes a specific prefix from a string and trims whitespace.

    Args:
        field_str (str): The original string (e.g., "Size: M").
        prefix (str): The prefix to remove (e.g., "Size:").

    Returns:
        str: Cleaned string (e.g., "M").
    """
    return field_str.replace(prefix, "").strip()


def is_valid_item(item):
    """
    Validates a raw data item by checking required fields and filtering out invalid values.

    Args:
        item (dict): A dictionary containing raw product data.

    Returns:
        bool: True if item is valid, otherwise False.
    """
    required_fields = ["Title", "Price", "Rating", "Colors", "Size", "Gender"]
    if any(item.get(field) is None for field in required_fields):
        return False
    if item["Title"] == "Unknown Product" or item["Price"] == "Price Unavailable":
        return False
    if "Invalid" in item["Rating"]:
        return False
    return True


def remove_duplicates(data):
    """
    Removes duplicate entries from a dataset based on Title, Price (IDR), and Rating.

    Args:
        data (list): A list of cleaned product dictionaries.

    Returns:
        list: A list with duplicate entries removed.
    """
    unique_data = []
    seen = set()

    for item in data:
        key = (item["Title"], item["Price (IDR)"], item["Rating"])
        if key not in seen:
            seen.add(key)
            unique_data.append(item)

    return unique_data


def clean_data(raw_data):
    """
    Cleans and transforms raw fashion product data.

    Args:
        raw_data (list): A list of raw product dictionaries scraped from the web.

    Returns:
        list: A cleaned list of dictionaries with normalized data and duplicates removed.
    """
    cleaned_data = []

    for item in raw_data:
        try:
            if not is_valid_item(item):
                continue

            cleaned_item = {
                "Title": item["Title"],
                "Price (IDR)": clean_price(item["Price"]),
                "Rating": clean_rating(item["Rating"]),
                "Colors": clean_colors(item["Colors"]),
                "Size": clean_field(item["Size"], "Size:"),
                "Gender": clean_field(item["Gender"], "Gender:"),
                "Timestamp": item.get("Timestamp"),
            }

            cleaned_data.append(cleaned_item)
        except Exception as e:
            print(f"Error cleaning item {item.get('Title', 'Unknown')}: {e}")
            continue

    return remove_duplicates(cleaned_data)


def convert_dtypes(df):
    """
    Convert specific DataFrame columns to appropriate data types.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the data to be type-converted.

    Returns
        df (pandas.DataFrame): The DataFrame with updated data types for applicable columns.
    """
    if "Price (IDR)" in df.columns:
        df["Price (IDR)"] = df["Price (IDR)"].astype("float64")
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
    return df
