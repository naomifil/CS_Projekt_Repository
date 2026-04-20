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
# --- Importierte Bibliotheken ---
import streamlit as st   # für das Web-App-Interface
import pandas as pd      # für Tabellen und Diagramme
import random            # um zufällige Fake-Daten zu erzeugen

# --- Titel ---
st.title("🌍 Air Quality Travel App (Demo-Version)")
st.markdown("Diese App ist eine Testversion ohne echte API-Daten. Sie zeigt, wie die finale App später aussehen wird.")

# --- Eingaben vom Nutzer ---
st.header("Benutzereingaben")
city = st.selectbox("Wähle eine Stadt:", ["Zurich", "Paris", "Beijing", "New York"])
asthma = st.selectbox("Wie stark ist dein Asthma?", ["Keins", "Leicht", "Mittel", "Stark"])
days = st.slider("Wie viele Tage in die Zukunft?", 1, 30)

# --- Fake-Daten-Generator ---
def generate_fake_aqi(days):
    """Erzeugt Fake-AQI-Werte für eine Anzahl Tage."""
    return [random.randint(20, 180) for _ in range(days)]

aqi_values = generate_fake_aqi(days)
average_aqi = sum(aqi_values) / len(aqi_values)

# --- Risiko-Berechnung ---
def calculate_risk(aqi, asthma_level):
    """Berechnet Risiko abhängig von Asthma und Luftqualität."""
    if asthma_level == "Stark":
        limit_high, limit_medium = 80, 50
    elif asthma_level == "Mittel":
        limit_high, limit_medium = 100, 70
    elif asthma_level == "Leicht":
        limit_high, limit_medium = 120, 90
    else:
        limit_high, limit_medium = 150, 100

    if aqi > limit_high:
        return "🔴 Hohes Risiko"
    elif aqi > limit_medium:
        return "🟡 Mittleres Risiko"
    else:
        return "🟢 Geringes Risiko"

risk = calculate_risk(average_aqi, asthma)

# --- Empfehlungen ---
def give_recommendation(risk):
    """Gibt eine Empfehlung, was zu tun ist."""
    if "Hohes" in risk:
        return "Nimm dein Inhalationsgerät mit und vermeide anstrengende Aktivitäten draußen. 😷"
    elif "Mittleres" in risk:
        return "Bleib vorsichtig, lüfte drinnen regelmäßig und beobachte dein Befinden."
    else:
        return "Alles gut 👍 — genieße deinen Aufenthalt!"

recommendation = give_recommendation(risk)

# --- Ergebnisse anzeigen ---
st.header("Ergebnisse")
st.write(f"**Stadt:** {city}")
st.write(f"**Durchschnittlicher (Fake) AQI:** {round(average_aqi, 1)}")
st.write(f"**Risikoeinschätzung:** {risk}")
st.info(recommendation)

# --- Diagramm anzeigen ---
st.subheader("Verlauf des (Fake) AQI in den nächsten Tagen")
df = pd.DataFrame({"Tag": list(range(1, days + 1)), "AQI": aqi_values})
st.line_chart(df.set_index("Tag"))
