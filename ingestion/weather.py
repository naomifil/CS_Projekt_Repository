from api_call import fetch_weather_batch


def insert_weather_measurements(conn, weather_results, location_ids):
    cursor = conn.cursor()

    for (lon, lat), data in zip(location_ids.keys(), weather_results.values()):
        location_id = location_ids[(lon, lat)]

        # daily forecast/history
        daily_df = data["daily"]

        for _, row in daily_df.iterrows():
            cursor.execute("""
                INSERT OR IGNORE INTO weather_daily (
                    location_id,
                    date,
                    temperature_mean,
                    relative_humidity_mean
                )
                VALUES (?, ?, ?, ?)
            """, (
                location_id,
                row["date"].strftime("%Y-%m-%d %H:%M:%S"),
                row["temperature_mean"],
                row["relative_humidity_mean"],
            ))


def ingest_weather(conn, coordinates, location_ids):
    results = fetch_weather_batch(
        [
            {"lat": lat, "lon": lon}
            for lon, lat in coordinates
        ]
    )

    insert_weather_measurements(conn, results, location_ids)