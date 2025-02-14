import requests
import pandas as pd
import json
import os
from datetime import datetime, timezone
from config import API_TOKEN

# Define target cities
CITIES = ["hanoi", "da-nang", "ho-chi-minh-city"]

# Set up local Data Lake directory
RAW_DATA_DIR = "data_lake/raw_data"
os.makedirs(RAW_DATA_DIR, exist_ok=True)

def safe_float(value):
    """Convert API values to float, returning None if invalid."""
    try:
        return float(value) if value not in ["-", "NaN", None] else None
    except (ValueError, TypeError):
        return None

def save_to_data_lake(city, data):
    """Save raw API response to a local Data Lake (JSON file)."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{RAW_DATA_DIR}/{city}_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"📂 Saved raw data for {city} → {filename}")

def fetch_aqi_data():
    """Fetch real-time air quality data for multiple cities and store in Data Lake."""
    all_data = []
    
    for city in CITIES:
        api_url = f"https://api.waqi.info/feed/{city}/?token={API_TOKEN}"
        response = requests.get(api_url)

        if response.status_code != 200:
            print(f"❌ API request for {city} failed with status code {response.status_code}")
            continue

        data = response.json()

        if data.get("status") != "ok":
            print(f"❌ API Error for {city}: {data.get('message', 'Unknown error')}")
            continue

        # 🔥 **Save raw API data to Data Lake before processing**
        save_to_data_lake(city, data)

        # Extract relevant fields safely
        city_data = data.get("data", {})
        station_info = city_data.get("city", {})
        iaqi = city_data.get("iaqi", {})

        station = station_info.get("name", "Unknown Station")
        geo = station_info.get("geo", [None, None])
        aqi = safe_float(city_data.get("aqi"))

        # Extract pollutants & weather data safely
        pm25 = safe_float(iaqi.get("pm25", {}).get("v"))
        pm10 = safe_float(iaqi.get("pm10", {}).get("v"))
        co = safe_float(iaqi.get("co", {}).get("v"))
        no2 = safe_float(iaqi.get("no2", {}).get("v"))
        o3 = safe_float(iaqi.get("o3", {}).get("v"))
        so2 = safe_float(iaqi.get("so2", {}).get("v"))
        temperature = safe_float(iaqi.get("t", {}).get("v"))
        humidity = safe_float(iaqi.get("h", {}).get("v"))
        wind_speed = safe_float(iaqi.get("w", {}).get("v"))
        pressure = safe_float(iaqi.get("p", {}).get("v"))

        # Handle missing dominant pollutant
        dominentpol = city_data.get("dominentpol", None)
        if not dominentpol:
            dominentpol = "unknown"

        # Handle missing timestamp
        time_info = city_data.get("time", {})
        time_measured = time_info.get("s")
        
        if not time_measured:
            time_measured = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            print(f"⚠️ Missing timestamp for {city}, using UTC {time_measured}")

        # Append valid data
        all_data.append({
            "station": station,
            "city": city,
            "aqi": aqi,
            "pm25": pm25,
            "pm10": pm10,
            "co": co,
            "no2": no2,
            "o3": o3,
            "so2": so2,
            "dominentpol": dominentpol,  # Fixed issue
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "pressure": pressure,
            "latitude": geo[0],
            "longitude": geo[1],
            "timestamp": datetime.strptime(time_measured, "%Y-%m-%d %H:%M:%S")
        })

    return pd.DataFrame(all_data) if all_data else None

# Run and check fetching
if __name__ == "__main__":
    df = fetch_aqi_data()
    if df is not None:
        print(df)
    else:
        print("❌ No data fetched.")
