import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from fetch_aqi import fetch_aqi_data

def store_data_in_postgres():
    """Fetch air quality data for multiple cities and store in PostgreSQL."""
    data = fetch_aqi_data()
    if data is None:
        print("❌ No data to store.")
        return

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )
        cur = conn.cursor()

        # SQL Insert Query (Updated for multiple cities)
        query = """
        INSERT INTO air_quality (station, city, aqi, pm25, pm10, co, no2, o3, so2, dominentpol, temperature, humidity, wind_speed, pressure, latitude, longitude, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (timestamp, city) DO UPDATE SET
            station = EXCLUDED.station,
            aqi = EXCLUDED.aqi,
            pm25 = EXCLUDED.pm25,
            pm10 = EXCLUDED.pm10,
            co = EXCLUDED.co,
            no2 = EXCLUDED.no2,
            o3 = EXCLUDED.o3,
            so2 = EXCLUDED.so2,
            dominentpol = EXCLUDED.dominentpol,
            temperature = EXCLUDED.temperature,
            humidity = EXCLUDED.humidity,
            wind_speed = EXCLUDED.wind_speed,
            pressure = EXCLUDED.pressure,
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude;
        """

        # Insert data for multiple cities
        for _, row in data.iterrows():
            cur.execute(query, (
                row["station"], row["city"], row["aqi"], row["pm25"], row["pm10"], row["co"],
                row["no2"], row["o3"], row["so2"], row["dominentpol"], row["temperature"],
                row["humidity"], row["wind_speed"], row["pressure"],
                row["latitude"], row["longitude"], row["timestamp"]
            ))

        conn.commit()
        cur.close()
        conn.close()
        print("✅ Data stored successfully for all cities.")

    except Exception as e:
        print(f"❌ Database insert failed: {e}")

# Run the storage function
if __name__ == "__main__":
    store_data_in_postgres()
