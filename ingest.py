import json
from database import create_tables, create_connection
from custom_db.locations import insert_locations
from custom_db.stations import insert_stations
from ingestion.air_quality import get_fresh_air_quality_measurements
from ingestion.weather import ingest_weather



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

    # locations
    location_ids = insert_locations(conn, coords)

    # stations
    # insert_stations(conn, station_map, location_ids)

    # fetch data and insert measurements
    get_fresh_air_quality_measurements(conn, coords, location_ids)
    ingest_weather(conn, coords, location_ids)

    conn.commit()
    conn.close()

    print("Ingestion complete")

