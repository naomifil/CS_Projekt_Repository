import sqlite3

DB_NAME = "air_quality2.db" # db with downloaded dataset for ml and fetched data api calls

# create connection to db
def create_connection():
    return sqlite3.connect(DB_NAME)

# creates db if not exist, db should be in the submitted zip
def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Locations, preloaded in database
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        latitude REAL,
        longitude REAL,
        UNIQUE(latitude, longitude)
    )
    """)

    # location level air quality with selected relevant data incl. units
    # here timestamp was set to current time stamp to avoid many missing values
    # because most stations only measure every few days (-> Limitation)
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
    """)    # station count -> we set a limit of max. 3 stations per location and only included stations
            # in a radius of 25km that measure all 3 features to avoid missing data

    # weather_daily includes historical data and forecast from API
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_daily (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER,

        date DATETIME,
        temperature_mean REAL,
        relative_humidity_mean REAL,

        FOREIGN KEY (location_id) REFERENCES locations(id),
        UNIQUE(location_id, date)
    )
    """)

    conn.commit()
    conn.close()
