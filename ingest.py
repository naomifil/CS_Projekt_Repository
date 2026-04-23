import json
from datetime import datetime, timezone
from api_call import get_aggregates_from_json
from database import create_tables, create_connection

# ---------------------------
# 1. Insert locations
# ---------------------------
def insert_locations(conn, coordinates):
    cursor = conn.cursor()
    location_ids = {}

    for lon, lat in coordinates:

        # insert only if not exists (based on lat/lon uniqueness)
        cursor.execute("""
            INSERT OR IGNORE INTO locations (name, latitude, longitude)
            VALUES (?, ?, ?)
        """, (f"{lat},{lon}", lat, lon))

        # fetch existing or newly inserted row
        cursor.execute("""
            SELECT id FROM locations
            WHERE latitude = ? AND longitude = ?
        """, (lat, lon))

        row = cursor.fetchone()
        if row:
            location_ids[(lon, lat)] = row[0]

    return location_ids

# ---------------------------
# 2. Insert stations (from JSON)
# ---------------------------
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


# ---------------------------
# 3. Insert measurements
# ---------------------------
def insert_measurements(conn, results, location_ids):
    cursor = conn.cursor()

    for (lon, lat), agg in results.items():
        readings = agg.readings
        station_count = agg.station_count

        location_id = location_ids[(lon, lat)]

        pm25 = readings.get("pm25")
        pm10 = readings.get("pm10")
        o3 = readings.get("o3")

        def val(x): return x.value if x else None
        def unit(x): return x.units if x else None

        timestamp = datetime.now(timezone.utc).isoformat()

        cursor.execute("""
            INSERT OR IGNORE INTO air_quality (
                location_id,
                pm25, pm10, o3,
                units_pm25, units_pm10, units_o3,
                station_count,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            location_id,
            val(pm25), val(pm10), val(o3),
            unit(pm25), unit(pm10), unit(o3),
            station_count,
            timestamp,
        ))

PARAMETERS = ["o3", "pm25", "pm10"]

def ingest_latest(conn, coordinates):
    from api_call import fetch_air_quality

    # 1. ensure locations exist
    location_ids = insert_locations(conn, coordinates)

    # 2. fetch aggregated data per coordinate
    results = fetch_air_quality(
        coordinates=coordinates,
        radius=20000,
        limit=5,
        parameters=PARAMETERS,
    )

    # 3. store directly
    insert_measurements(conn, results, location_ids)

    conn.commit()

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    create_tables()

    # same coordinates as before
    coords = [
        (2.3522, 48.8566),
        (8.5417, 47.3769),
        (13.4050, 52.5200),
        (-0.1278, 51.5074),
        (8.6821, 50.1109),
        (4.3517, 50.8503),
        (18.0686, 59.3293),
    ]

    # load station cache
    with open("stations.json") as f:
        station_map = json.load(f)

    # open a connection
    conn = create_connection()

    # 1. locations
    location_ids = insert_locations(conn, coords)

    # 2. stations
    # insert_stations(conn, station_map, location_ids)

    # 3. fetch API data
    results = get_aggregates_from_json(PARAMETERS)

    # 4. insert measurements
    insert_measurements(conn, results, location_ids)

    conn.commit()
    conn.close()

    print("Ingestion complete")