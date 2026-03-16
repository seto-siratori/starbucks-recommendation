"""
Starbucks menu data collection and processing.
Downloads public nutrition CSV from GitHub and adds statistically generated
price and seasonal columns.
"""
import pandas as pd
import numpy as np
import os

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

# Source: public dataset from GitHub (reisanar/datasets)
CSV_URL = "https://raw.githubusercontent.com/reisanar/datasets/master/starbucks.csv"


def download_and_process():
    df = pd.read_csv(CSV_URL)
    df.columns = df.columns.str.strip()

    # --- Map size from Beverage_prep ---
    size_map = {
        "Short": "Short",
        "Tall": "Tall",
        "Grande": "Grande",
        "Venti": "Venti",
    }

    def extract_size(prep):
        prep_str = str(prep)
        for key in size_map:
            if key in prep_str:
                return size_map[key]
        return "Grande"  # default

    df["size"] = df["Beverage_prep"].apply(extract_size)

    # --- Statistically generate price based on category and size ---
    np.random.seed(42)

    # Base price by category (USD, realistic Starbucks pricing)
    category_base_price = {
        "Coffee": 2.45,
        "Classic Espresso Drinks": 4.25,
        "Signature Espresso Drinks": 5.15,
        "Tazo® Tea Drinks": 3.75,
        "Shaken Iced Beverages": 4.45,
        "Smoothies": 5.25,
        "Frappuccino® Blended Coffee": 4.95,
        "Frappuccino® Blended Crème": 4.95,
        "Frappuccino® Light Blended Coffee": 4.75,
    }

    size_multiplier = {
        "Short": 0.80,
        "Tall": 0.90,
        "Grande": 1.00,
        "Venti": 1.10,
    }

    def generate_price(row):
        base = category_base_price.get(row["Beverage_category"], 4.50)
        mult = size_multiplier.get(row["size"], 1.0)
        noise = np.random.normal(0, 0.15)
        return round(base * mult + noise, 2)

    df["price_usd"] = df.apply(generate_price, axis=1)

    # --- Statistically generate seasonal flag ---
    # Frappuccinos and some specialty drinks more likely to be seasonal
    seasonal_keywords = [
        "Pumpkin", "Peppermint", "Caramel Brulée", "Eggnog",
        "Gingerbread", "Chestnut", "Toasted", "Holiday",
    ]

    def assign_seasonal(row):
        name = str(row["Beverage"])
        # Keyword-based: certain flavors are seasonal
        for kw in seasonal_keywords:
            if kw.lower() in name.lower():
                return 1
        # Probabilistic: Frappuccinos 15% chance, others 5%
        if "Frappuccino" in str(row["Beverage_category"]):
            return int(np.random.random() < 0.15)
        return int(np.random.random() < 0.05)

    df["seasonal_flag"] = df.apply(assign_seasonal, axis=1)

    # --- Select and rename to required columns ---
    result = pd.DataFrame({
        "product_name": df["Beverage"],
        "category": df["Beverage_category"],
        "size": df["size"],
        "price_usd": df["price_usd"],
        "calories": pd.to_numeric(df["Calories"], errors="coerce"),
        "sugar_g": pd.to_numeric(df["Sugars (g)"], errors="coerce"),
        "caffeine_mg": pd.to_numeric(df["Caffeine (mg)"], errors="coerce"),
        "seasonal_flag": df["seasonal_flag"],
    })

    out_path = os.path.join(RAW_DIR, "starbucks_menu.csv")
    result.to_csv(out_path, index=False)
    print(f"Saved {len(result)} rows to {out_path}")
    print(f"Columns: {list(result.columns)}")
    print(f"Categories: {result['category'].nunique()}")
    print(f"Seasonal items: {result['seasonal_flag'].sum()}")
    return result


if __name__ == "__main__":
    download_and_process()
