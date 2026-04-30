from datetime import datetime, timezone
from api_call import fetch_air_quality

PARAMETERS = ["o3", "pm25", "pm10"]


def insert_measurements(conn, results, location_ids):
    cursor = conn.cursor()

    for entry in results:
        lon, lat = entry.coordinate
        agg = entry

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


def ingest_latest(conn, coordinates, location_ids):
    results = fetch_air_quality(
        coordinates=coordinates,
        radius=20000,
        limit=5,
        parameters=PARAMETERS,
    )

    insert_measurements(conn, results, location_ids)