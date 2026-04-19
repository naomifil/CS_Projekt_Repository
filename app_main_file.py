import streamlit as st
from api_call import fetch_air_quality
from database import create_tables

st.write ("Welcome to our App")
st.write ("This is a tool to help you analyze health risks based on local air quality")

# This will create the empty database if it does not exist yet
create_tables()

# This is going to change, am still working on some improvements:
# - Instead of multiple round-trips per location, we will identify the relevant stations manually
#   and add them to the database. The api will then only query the stations listed in the database to optimize
#   how many calls are needed (API Rate limit 60/min - 2000/hr).

LOCATIONS = {
    "St.Gallen": (9.375902, 47.432292),
    "Zürich":     (8.541694, 47.376887),
    "Bern":       (7.447447, 46.947974),
    "Genf":       (6.143158, 46.204391),
}

PARAMETERS=["o3", "pm25", "pm10"]

# --- fetch_air_quality: averaged readings for multiple coordinates at once ---
results = fetch_air_quality(
    coordinates=list(LOCATIONS.values()),
    radius=5000,
    limit=5,
    parameters=PARAMETERS,
)

for name, entry in zip(LOCATIONS.keys(), results):
    st.write(f"\n{name} {entry["coordinate"]}  [{entry["station_count"]} station(s)]")
    if entry["readings"]:
        for param, reading in entry["readings"].items():
            st.write(f"  {param:<6} {reading["value"]:.2f} {reading["units"] or ''}")
    else:
        st.write("  No readings for requested parameters.")
