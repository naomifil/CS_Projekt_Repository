"""
AirSense – User Interface

This Streamlit user interface was developed by the author and partially supported
with AI assistance from ChatGPT (OpenAI).

The use of AI included:
- Structuring and refactoring selected code sections
- Debugging support
- Improving readability and code comments
- Writing and revising user-facing information texts and code explanations
- Optimizing selected repeated UI and data-processing logic

Sections that were generated or substantially rewritten with the help of ChatGPT
are marked directly in the code with:
    # --- AI-assisted section (ChatGPT/OpenAI)

All design decisions, testing, integration, final adjustments and responsibility
for the submitted version were carried out by the author.
"""

import streamlit as st
from datetime import date, timedelta
import pandas as pd
from api_and_db import fetch_weather, create_openmeteo_client
from ml_model_db import train_model_for_city, predict_multiple_days
from risk_module import calculate_total_risk

# Page setup: defines general Streamlit layout and browser title
st.set_page_config(
    page_title="AirSense",
    page_icon=":earth_africa:", # 🌍 Erde Emoji
    layout="wide")

# Basic city data: stores coordinates and ids needed for weather API and machine learning model
# --- AI-generated section (ChatGPT/OpenAI) ---
ORTE = {
    "Zürich": (8.5417, 47.3769),
    "Paris": (2.3522, 48.8566),
    "Berlin": (13.4050, 52.5200),
    "London": (-0.1278, 51.5074),
    "Frankfurt": (8.6821, 50.1109),
    "Brüssel": (4.3517, 50.8503),
    "Stockholm": (18.0686, 59.3293)}
## for the ML model
ORT_IDS = {
    "Paris": "1",
    "Zürich": "2",
    "Berlin": "3",
    "London": "4",
    "Frankfurt": "5",
    "Brüssel": "6",
    "Stockholm": "7"}

VERFUEGBARE_ORTE = ["Paris", "London", "Frankfurt", "Brüssel", "Stockholm"]

PARAMETER = ["pm25", "pm10", "o3"]
# --- End AI-generated section ---

MAX_FORECAST_TAGE = 14

MAX_RISIKO_SCORE = 105000

# Risk design: returns fitting colours and emoji for the different risk levels
# --- AI-generated section (ChatGPT/OpenAI) ---
def hole_risiko_design(farbe):
    if farbe == "Grün":
        return "🟢", "#e8f5e9", "#2e7d32"
    elif farbe == "Gelb":
        return "🟡", "#fffde7", "#f9a825"
    elif farbe == "Orange":
        return "🟠", "#fff3e0", "#ef6c00"
    elif farbe == "Rot":
        return "🔴", "#ffebee", "#c62828"
    else:
        return "🟣", "#f3e5f5", "#6a1b9a"

# Cache ml model: avoids retraining the model after every Streamlit rerun
@st.cache_resource
def lade_ml_modell(location_id):
    model, mae, predictions = train_model_for_city(location_id)
    return model, mae

# Cache weather data: loads forecast data and stores it temporarily for better app performance
@st.cache_data(ttl=300)
def lade_wetterdaten(lat, lon, forecast_tage):
    client = create_openmeteo_client()
    wetter = fetch_weather(
        client,
        lat=lat,
        lon=lon,
        past_days=0,
        forecast_days=forecast_tage)
    return wetter
# --- End AI-generated section ---


# Sidebar navigation: lets the user switch between the main app pages
st.sidebar.title("Menü")
seite = st.sidebar.selectbox("Wähle eine Seite aus:",
    ["Startseite", "Eingaben", "Ergebnisse"])

st.sidebar.divider()

st.sidebar.markdown("**AirSense**")
st.sidebar.caption(
    "AirSense schätzt das persönliche Risiko anhand von Reisedaten, Wettervorhersage, "
    "ML-Vorhersage der Luftverschmutzung und Gesundheitsangaben."
)

st.sidebar.divider()



st.sidebar.markdown("**Ablauf:**")
st.sidebar.caption("1. Eingaben speichern")
st.sidebar.caption("2. Ergebnisse laden")
st.sidebar.caption("3. Methodik nachlesen")


# Start page: explains the idea of the app and how the user should use it
if seite == "Startseite":
    st.title("AirSense: eine Luftqualitäts-App für Reisen")
    st.header("Startseite")
    st.markdown(
        "Diese App hilft dir dabei, **vor einer Reise** nochmals zu überprüfen, "
        "wie hoch das mögliche Risiko durch Luftverschmutzung am **Reiseziel** sein könnte. "
        "So kannst du deine Reiseplanung besser einschätzen und entscheiden, "
        "ob du deine Aktivitäten anpassen solltest.")



    st.subheader("So benutzt du die App")

    st.markdown("""
    1. 👈 Gehe links im Menü auf **Eingaben**.
    2. Gib dort dein ***Alter***, dein ***Asthma-Level***, dein ***Aktivitätslevel*** und deine ***Reisedaten*** ein.
    3. Wähle den ***Ort*** aus, für den du das Risiko einschätzen möchtest.
    4. Gehe danach links im Menü auf **Ergebnisse**, um deinen Risikoscore und eine Empfehlung zu sehen.
    """)

    st.warning("Wichtig: Die App gibt nur eine grobe Einschätzung und ersetzt keine ärztliche Beratung.")

    st.divider()

    st.subheader("Mehr über die App")

    st.markdown("""
        Du hast zwei Möglichkeiten, mehr zu erfahren:
        - 👈 **Links über dem Menü** auf **Methodik** klicken (immer sichtbar)
        - 👇 **Unten** auf den Button **Methodik** klicken

        Dort wird erklärt, wie die App im Hintergrund arbeitet und wie die Risikoeinschätzung berechnet wird.
        """)

    # Methodik button: links to the extra page where users can read how the app works in the background
    st.page_link("pages/Methodik.py", label="Methodik", icon="📚")

# Input page: collects personal and travel data needed for the risk calculation
elif seite == "Eingaben":
    st.write("Hier kannst du deine Daten eingeben.")

    st.title("Deine Reisedaten")
    st.markdown("Damit die App eine persönliche Einschätzung geben kann, brauchen wir einige Angaben zu deiner Reise und zu deinem Gesundheitsprofil.")
    st.write("Die Informationen werden später verwendet, um die Luftqualität am gewählten Ort mit deinem Asthma-Level und deiner geplanten Aktivität zu verbinden.")

    st.divider()

    st.header("Eingaben")
    st.info("Je genauer die Angaben sind, desto besser kann die App später eine persönliche Einschätzung anzeigen.")

    # Setup: two columns for input
    col1, col2 = st.columns(2)

    # Personal input: asks for health-related information that influences the final risk score
    with col1:
        st.subheader("Persönliche Angaben")
        st.caption("Diese Angaben helfen einzuschätzen, wie empfindlich du reagieren könntest.")

        alter = st.number_input("Wie alt bist du?", min_value=0, max_value=100)

        asthma_level = st.selectbox(
            "Wie stark ist dein Asthma?",
            ["Kein Asthma", "Leicht", "Mittel", "Stark"])

        aktivitaet = st.selectbox(
            "Wie aktiv möchtest du in den Ferien sein?",
            ["Nicht aktiv", "Aktiv", "Sehr aktiv"])

    # Travel input: asks for destination and travel dates within the available forecast range
    with col2:
        st.subheader("Reiseangaben")
        st.caption("Diese Angaben beschreiben, wohin und wann du reisen möchtest.")

        heute = date.today()
        max_datum = heute + timedelta(days=MAX_FORECAST_TAGE)

        ort = st.selectbox(
            "Wähle deinen Reiseort:",
            VERFUEGBARE_ORTE)

        reise_start = st.date_input("Wann beginnt deine Reise?", min_value=heute, max_value=max_datum)

        reise_ende = st.date_input(
            "Wann endet deine Reise?",
            min_value=reise_start, max_value=max_datum)

        st.caption("Hinweis: Die App erlaubt aktuell nur Reisedaten innerhalb der nächsten 14 Tage, weil die Wettervorhersage nur für einen begrenzten Zeitraum verfügbar ist.")

    # Save inputs: stores user data in session state so it can be used on the results page
    if st.button("Eingaben speichern"):
        st.session_state["alter"] = alter
        st.session_state["asthma_level"] = asthma_level
        st.session_state["aktivitaet"] = aktivitaet
        st.session_state["ort"] = ort
        st.session_state["reise_start"] = reise_start
        st.session_state["reise_ende"] = reise_ende
        st.success("Deine Eingaben wurden gespeichert.")

    st.info("Wenn du alle Daten eingegeben hast, kannst du links im Menü auf Ergebnisse klicken, um deine Risikoeinschätzung zu sehen.")

# Results page: loads weather data, predicts air pollution and calculates the personal risk score
else:
    st.write("Hier kannst du dir deine Ergebnisse anschauen.")
    st.title("Deine persönliche Risikoeinschätzung")

    if "alter" in st.session_state:

        # Saved input overview: shows the user which data will be used for the calculation
        st.subheader("Gespeicherte Eingaben")
        st.write("Stimmen diese Daten? Du kannst auf 'Eingaben' zurückgehen, um etwas zu ändern.")

        col1, col2 = st.columns(2)

        with col1:
            st.write("Alter:", st.session_state["alter"])
            st.write("Asthma-Level:", st.session_state["asthma_level"])
            st.write("Aktivitätslevel:", st.session_state["aktivitaet"])

        with col2:
            st.write("Ort:", st.session_state["ort"])
            st.write("Reisebeginn:", st.session_state["reise_start"])
            st.write("Reiseende:", st.session_state["reise_ende"])

        st.divider()

        ort_name = st.session_state["ort"]
        lon, lat = ORTE[ort_name]

        # Weather data: loads forecast data for the selected destination
        if st.button("Ergebnisse laden"):
            try:
                wetter = lade_wetterdaten(
                    lat=lat,
                    lon=lon,
                    forecast_tage=MAX_FORECAST_TAGE
                )
                # Data filtering and prediction: keeps only travel days and predicts pollutant levels
                # --- AI-generated section (ChatGPT/OpenAI)
                wetter_tabelle = wetter["daily"]

                wetter_tabelle["datum"] = pd.to_datetime(wetter_tabelle["date"]).dt.date

                reise_start = st.session_state["reise_start"]
                reise_ende = st.session_state["reise_ende"]

                wetter_reise = wetter_tabelle[
                    (wetter_tabelle["datum"] >= reise_start) &
                    (wetter_tabelle["datum"] <= reise_ende)
                    ]

                location_id = ORT_IDS[ort_name]
                model, mae = lade_ml_modell(location_id)
                vorhersage = predict_multiple_days(model, wetter_reise)

                risiko_scores = []
                risiko_levels = []
                farben = []
                empfehlungen = []

                for index, zeile in vorhersage.iterrows():
                    risiko_score, risiko_level, farbe, empfehlung = calculate_total_risk(
                        pm25=zeile["pm25"],
                        pm10=zeile["pm10"],
                        o3=zeile["o3"],
                        temperature=zeile["temperature_mean"],
                        humidity=zeile["relative_humidity_mean"],
                        alter=st.session_state["alter"],
                        aktivitaet=st.session_state["aktivitaet"],
                        asthma_level=st.session_state["asthma_level"]
                    )

                    risiko_scores.append(risiko_score)
                    risiko_levels.append(risiko_level)
                    farben.append(farbe)
                    empfehlungen.append(empfehlung)

                vorhersage["risiko_score"] = risiko_scores
                vorhersage["risiko_level"] = risiko_levels
                vorhersage["farbe"] = farben
                vorhersage["empfehlung"] = empfehlungen

                schlimmster_tag = vorhersage.loc[vorhersage["risiko_score"].idxmax()]

                # Main result card: highlights the most critical day of the trip
                st.divider()
                st.subheader("Tägliche Risikoeinschätzung")

                emoji, hintergrund_farbe, text_farbe = hole_risiko_design(schlimmster_tag["farbe"])

                st.markdown(
                    f"""
                    <div style="
                        background-color: {hintergrund_farbe};
                        padding: 24px;
                        border-radius: 18px;
                        border-left: 8px solid {text_farbe};
                        margin-bottom: 20px;
                    ">
                        <h2 style="color: {text_farbe}; margin-bottom: 8px;">
                            {emoji} {schlimmster_tag["risiko_level"]}es Risiko
                        </h2>
                        <p style="font-size: 18px; margin-bottom: 10px;">
                            Der kritischste Tag deiner Reise ist der 
                            <b>{schlimmster_tag["datum"].strftime("%d.%m.%Y")}</b>.
                        </p>
                        <p style="font-size: 16px;">
                            {schlimmster_tag["empfehlung"]}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                # --- End AI-generated section
                # Result metrics: gives a quick overview of the most important values
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Höchster Risiko-Score", round(schlimmster_tag["risiko_score"], 2))
                    st.caption("Der maximal mögliche Risiko-Score ist 105'000")

                with col2:
                    st.metric("Kritischster Tag", schlimmster_tag["datum"].strftime("%d.%m.%Y"))

                with col3:
                    st.metric("Risikostufe", schlimmster_tag["risiko_level"])

                # Risk chart: shows how the personal risk changes over the travel period
                st.subheader("Risikoverlauf während der Reise")

                risiko_graph = vorhersage[["datum", "risiko_score"]].copy()
                risiko_graph = risiko_graph.set_index("datum")

                if len(vorhersage) > 1:
                    st.line_chart(risiko_graph)
                else:
                    st.metric("Risiko-Score für diesen Tag", round(schlimmster_tag["risiko_score"], 2))
                    st.bar_chart(risiko_graph)

                # Pollutants on worst day: shows which pollution values were predicted on the most critical day
                st.subheader("Schadstoffe am kritischsten Tag")

                schadstoffe_schlimmster_tag = pd.DataFrame({
                    "Schadstoff": ["PM2.5", "PM10", "Ozon"],
                    "Wert": [
                        schlimmster_tag["pm25"],
                        schlimmster_tag["pm10"],
                        schlimmster_tag["o3"]
                    ]
                })

                schadstoffe_schlimmster_tag = schadstoffe_schlimmster_tag.set_index("Schadstoff")
                st.bar_chart(schadstoffe_schlimmster_tag)

                # Daily overview: shows a short recommendation for every travel day
                # --- AI-generated section (ChatGPT/OpenAI) ---
                st.subheader("Übersicht pro Reisetag")

                for index, tag in vorhersage.iterrows():
                    emoji, hintergrund_farbe, text_farbe = hole_risiko_design(tag["farbe"])

                    with st.container(border=True):
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.markdown(f"### {emoji}")

                        with col2:
                            st.markdown(f"**{tag['datum'].strftime('%d.%m.%Y')}**")
                            st.write(f"Risiko: **{tag['risiko_level']}**")

                        with col3:
                            st.write(tag["empfehlung"])
                            st.caption(
                                f"PM2.5: {tag['pm25']:.1f} | "
                                f"PM10: {tag['pm10']:.1f} | "
                                f"O₃: {tag['o3']:.1f}"
                            )

                with st.expander("Tägliche Risikodaten anzeigen"):
                    st.dataframe(
                        vorhersage[[
                            "datum",
                            "temperature_mean",
                            "relative_humidity_mean",
                            "pm25",
                            "pm10",
                            "o3",
                            "risiko_score",
                            "risiko_level",
                            "farbe"
                        ]],
                        use_container_width=True,
                        hide_index=True
                    )
                # --- End AI-generated section ---
                # Pollution prediction: displays the air pollution values predicted by the ml model
                st.divider()
                st.subheader("Vorhergesagte Luftverschmutzung")

                st.write("Das Modell schätzt aus den Wetterdaten die Luftverschmutzung für deine Reisetage.")
                st.caption(f"Durchschnittlicher Modellfehler im Test: {mae:.2f}")

                st.dataframe(
                    vorhersage[["datum", "pm25", "pm10", "o3"]],
                    use_container_width=True,
                    hide_index=True
                )

                st.subheader("Vorhergesagte Schadstoffe")
                # Pollution chart: visualizes predicted pollutant values for one or multiple travel days
                # --- AI-generated section --> AI used to restructure from line chart only to bar chart for one day trips (ChatGPT/OpenAI) ---

                if len(vorhersage) > 1:
                    schadstoff_graph = vorhersage[["datum", "pm25", "pm10", "o3"]].copy()
                    schadstoff_graph = schadstoff_graph.set_index("datum")

                    st.line_chart(schadstoff_graph)

                else:
                    einzelner_tag = vorhersage.iloc[0]

                    col1, col2, col3 = st.columns(3)

                    col1.metric("PM2.5", f"{einzelner_tag['pm25']:.1f}")
                    col2.metric("PM10", f"{einzelner_tag['pm10']:.1f}")
                    col3.metric("Ozon", f"{einzelner_tag['o3']:.1f}")

                    schadstoffe_einzel_tag = pd.DataFrame({
                        "Schadstoff": ["PM2.5", "PM10", "Ozon"],
                        "Wert": [
                            einzelner_tag["pm25"],
                            einzelner_tag["pm10"],
                            einzelner_tag["o3"]
                        ]
                    })

                    schadstoffe_einzel_tag = schadstoffe_einzel_tag.set_index("Schadstoff")
                    st.bar_chart(schadstoffe_einzel_tag)
                # --- End AI-generated section ---
                # Weather output: shows the weather data that was used as model input
                st.divider()
                st.subheader("Wettervorhersage für deine Reise")

                st.write("Wetterdaten für:", ort_name)

                durchschnitt_temp = wetter_reise["temperature_mean"].mean()
                durchschnitt_feuchtigkeit = wetter_reise["relative_humidity_mean"].mean()
                anzahl_tage = len(wetter_reise)

                col1, col2, col3 = st.columns(3)

                col1.metric("Reisetage", anzahl_tage)


                col2.metric("Ø Temperatur", f"{durchschnitt_temp:.1f} °C")

                col3.metric("Ø Luftfeuchtigkeit", f"{durchschnitt_feuchtigkeit:.1f} %")

                st.caption(
                    "Diese Wetterdaten werden später als Grundlage für die Vorhersage der Luftverschmutzung verwendet."
                )

                st.subheader("Wetter während der Reise")
                # --- AI-generated section --> AI used to restructure from line chart only to bar chart for one day trips (ChatGPT/OpenAI) ---
                if len(wetter_reise) > 1:
                    st.subheader("Temperatur:")
                    temperatur_graph = wetter_reise[["datum", "temperature_mean"]].copy()
                    temperatur_graph = temperatur_graph.set_index("datum")
                    st.line_chart(temperatur_graph)

                    st.subheader("Luftfeuchtigkeit:")
                    feuchtigkeit_graph = wetter_reise[["datum", "relative_humidity_mean"]].copy()
                    feuchtigkeit_graph = feuchtigkeit_graph.set_index("datum")
                    st.line_chart(feuchtigkeit_graph)

                else:
                    einzelner_tag = wetter_reise.iloc[0]

                    col1, col2 = st.columns(2)

                    col1.metric("Temperatur an diesem Tag", f"{einzelner_tag['temperature_mean']:.1f} °C")
                    col2.metric("Luftfeuchtigkeit an diesem Tag", f"{einzelner_tag['relative_humidity_mean']:.1f} %")

                    wetter_einzel_tag = pd.DataFrame({
                        "Wetterwert": ["Temperatur", "Luftfeuchtigkeit"],
                        "Wert": [
                            einzelner_tag["temperature_mean"],
                            einzelner_tag["relative_humidity_mean"]
                        ]
                    })

                    wetter_einzel_tag = wetter_einzel_tag.set_index("Wetterwert")
                    st.bar_chart(wetter_einzel_tag)
                # --- End AI-generated section ---
                with st.expander("Wetterdaten als Tabelle anzeigen"):
                    st.dataframe(
                        wetter_reise[["datum", "temperature_mean", "relative_humidity_mean"]],
                        use_container_width=True,
                        hide_index=True
                    )

            # Error handling: gives understandable feedback if data or calculations fail
            except ValueError as fehler:
                st.error("Für diesen Ort gibt es aktuell nicht genügend Daten für das ML-Modell.")
                st.write("Bitte versuche es mit einem anderen Ort.")
                st.caption(f"Technische Fehlermeldung: {fehler}")

            except Exception as fehler:
                st.error("❌ Die Ergebnisse konnten nicht berechnet werden.")
                st.write("Fehlermeldung:", fehler)

        else:
            st.info(
                "Klicke auf den Button, um Wetterdaten, Luftverschmutzung und dein persönliches Risiko zu berechnen.")

    else:
        st.warning("Bitte gehe zuerst auf die Seite Eingaben und speichere deine Angaben.")

