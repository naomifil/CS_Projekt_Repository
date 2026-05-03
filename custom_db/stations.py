def insert_stations(conn, station_map, location_ids):
    cursor = conn.cursor()

    for key, stations in station_map.items():
        lon, lat = map(float, key.split(","))
        location_id = location_ids[(lon, lat)]

        for station in stations:
            cursor.execute("""
                INSERT OR IGNORE INTO stations (
                    location_id, station_api_id, name
                )
                VALUES (?, ?, ?)
            """, (
                location_id,
                station["id"],
                station["name"],
            ))