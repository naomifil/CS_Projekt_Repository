from api_call import fetch_weather_batch


def insert_weather_measurements(conn, weather_results, location_ids):
    cursor = conn.cursor()

    for (lon, lat), data in zip(location_ids.keys(), weather_results.values()):
        location_id = location_ids[(lon, lat)]

        current = data["current"]

        cursor.execute("""
            INSERT INTO weather (
                location_id,
                temperature_2m,
                relative_humidity_2m,
                timestamp
            )
            VALUES (?, ?, ?, ?)
        """, (
            location_id,
            current["temperature_2m"],
            current["relative_humidity_2m"],
            current["time"],
        ))


def ingest_weather(conn, coordinates, location_ids):
    results = fetch_weather_batch(
        [
            {"lat": lat, "lon": lon}
            for lon, lat in coordinates
        ]
    )

    insert_weather_measurements(conn, results, location_ids)