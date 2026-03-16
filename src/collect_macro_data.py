"""
Macro indicator data collection.
- FRED: CPI (CPIAUCSL) and Average Hourly Earnings (CES0500000003) as real wage proxy
- Open-Meteo: Temperature data for major US cities
"""
import pandas as pd
import requests
import os
from datetime import datetime, timedelta

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def fetch_fred_series(series_id, start_date, end_date):
    """Fetch data from FRED public CSV download endpoint (no API key needed)."""
    url = (
        f"https://fred.stlouisfed.org/graph/fredgraph.csv"
        f"?id={series_id}&cosd={start_date}&coed={end_date}"
    )
    df = pd.read_csv(url)
    df.columns = ["date", series_id]
    df["date"] = pd.to_datetime(df["date"])
    df[series_id] = pd.to_numeric(df[series_id], errors="coerce")
    return df


def collect_fred_data():
    """Collect CPI and wage index from FRED (monthly, past 5 years)."""
    end_date = "2026-03-01"
    start_date = "2021-03-01"

    print("Fetching CPI (CPIAUCSL) from FRED...")
    cpi = fetch_fred_series("CPIAUCSL", start_date, end_date)

    print("Fetching Average Hourly Earnings (CES0500000003) from FRED...")
    wages = fetch_fred_series("CES0500000003", start_date, end_date)

    # Merge on date
    merged = pd.merge(cpi, wages, on="date", how="outer").sort_values("date")
    merged.columns = ["date", "cpi", "avg_hourly_earnings"]

    # Compute real wage index (earnings / CPI * 100)
    merged["real_wage_index"] = (
        merged["avg_hourly_earnings"] / merged["cpi"] * 100
    ).round(4)

    out_path = os.path.join(RAW_DIR, "fred_macro.csv")
    merged.to_csv(out_path, index=False)
    print(f"Saved {len(merged)} rows to {out_path}")
    return merged


def collect_weather_data():
    """Collect daily temperature from Open-Meteo for major US cities (past 2 years)."""
    cities = {
        "New York": (40.7128, -74.0060),
        "Los Angeles": (34.0522, -118.2437),
        "Chicago": (41.8781, -87.6298),
        "Houston": (29.7604, -95.3698),
        "Seattle": (47.6062, -122.3321),
    }

    end_date = "2026-03-15"
    start_date = "2024-03-15"

    all_data = []
    for city, (lat, lon) in cities.items():
        print(f"Fetching weather for {city}...")
        url = (
            f"https://archive-api.open-meteo.com/v1/archive"
            f"?latitude={lat}&longitude={lon}"
            f"&start_date={start_date}&end_date={end_date}"
            f"&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min"
            f"&temperature_unit=fahrenheit"
            f"&timezone=America/New_York"
        )
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()

        daily = data["daily"]
        df = pd.DataFrame({
            "date": daily["time"],
            "temp_mean_f": daily["temperature_2m_mean"],
            "temp_max_f": daily["temperature_2m_max"],
            "temp_min_f": daily["temperature_2m_min"],
        })
        df["city"] = city
        all_data.append(df)

    result = pd.concat(all_data, ignore_index=True)
    result["date"] = pd.to_datetime(result["date"])

    out_path = os.path.join(RAW_DIR, "weather_daily.csv")
    result.to_csv(out_path, index=False)
    print(f"Saved {len(result)} rows to {out_path}")
    return result


if __name__ == "__main__":
    collect_fred_data()
    collect_weather_data()
