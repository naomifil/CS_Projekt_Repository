import sqlite3

DB_NAME = "air_quality.db"

def create_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Locations (user-defined or query-based areas)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        latitude REAL,
        longitude REAL
    )
    """)

    # Stations (actual monitoring stations)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER,
        station_api_id INTEGER,   -- ID from OpenAQ (or your API)
        name TEXT,
        latitude REAL,
        longitude REAL,
        FOREIGN KEY (location_id) REFERENCES locations(id)
    )
    """)

    # Air quality measurements per station
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS air_quality (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_id INTEGER,
        parameter TEXT,
        value REAL,
        units TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (station_id) REFERENCES stations(id)
    )
    """)

    conn.commit()
    conn.close()
