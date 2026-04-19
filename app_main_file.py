import streamlit as st
from api_call import fetch_air_quality

st.write ("Welcome to our App")
st.write ("This is a tool to help you book your business trip")

st.write (""" Please enter your departure place, destination office and start date to get started. 
          We'll show you your flight options. """)

LOCATIONS = {
    "Weinfelden": (9.108883, 47.567735),
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
