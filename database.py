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
        longitude REAL,
        UNIQUE(latitude, longitude)
    )
    """)

    # location level air quality
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS air_quality (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER,

        pm25 REAL,
        pm10 REAL,
        o3 REAL,

        units_pm25 TEXT,
        units_pm10 TEXT,
        units_o3 TEXT,

        station_count INTEGER,  -- how many stations contributed

        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (location_id) REFERENCES locations(id),
        UNIQUE(location_id, timestamp)
    )
    """)

    conn.commit()
    conn.close()
