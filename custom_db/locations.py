def insert_locations(conn, coordinates):
    cursor = conn.cursor()
    location_ids = {}

    for lon, lat in coordinates:

        cursor.execute("""
            INSERT OR IGNORE INTO locations (name, latitude, longitude)
            VALUES (?, ?, ?)
        """, (f"{lat},{lon}", lat, lon))

        cursor.execute("""
            SELECT id FROM locations
            WHERE latitude = ? AND longitude = ?
        """, (lat, lon))

        row = cursor.fetchone()
        if row:
            location_ids[(lon, lat)] = row[0]

    return location_ids