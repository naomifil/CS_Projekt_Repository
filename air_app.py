import streamlit as st
from api_call import fetch_air_quality



##Dictionary code gemacht von ChatGPT
ORTE = {
    "Zürich": (8.5417, 47.3769),
    "Paris": (2.3522, 48.8566),
    "Berlin": (13.4050, 52.5200),
    "London": (-0.1278, 51.5074),
    "Frankfurt": (8.6821, 50.1109),
    "Brüssel": (4.3517, 50.8503),
    "Stockholm": (18.0686, 59.3293)}

PARAMETER = ["pm25", "pm10", "o3"]
##Ende ChatGPT


st.set_page_config(
    page_title="Luftqualitäts-App",
    layout="wide")

st.sidebar.title("Menü")
seite = st.sidebar.selectbox("Wähle eine Seite aus:",
    ["Startseite", "Eingaben", "Ergebnisse", "Methodik"])





if seite == "Startseite":
    st.title("Luftqualitäts-App für Reisen")
    st.header("Startseite")
    st.write("Willkommen in der Luftqualitäts-App. Diese App hilft dabei, das Risiko durch Luftverschmutzung während einer Reise einzuschätzen.")

    st.subheader("So benutzt du die App")
    ## folgender Text für seite (nicht der code) von ChatGPT erstellt
    st.markdown("""
    1. 👈 Gehe links im Menü auf **Eingaben**.
    2. Gib dort dein ***Alter***, dein ***Asthma-Level***, dein ***Aktivitätslevel*** und deine ***Reisedaten*** ein.
    3. Wähle den ***Ort*** aus, für den du das Risiko einschätzen möchtest.
    4. Gehe danach links im Menü auf **Ergebnisse**, um deinen Risikoscore und eine Empfehlung zu sehen.
    """)

    st.warning("Wichtig: Die App gibt nur eine grobe Einschätzung und ersetzt keine ärztliche Beratung.")

    st.divider()

    st.subheader("Mehr über die App")

    st.markdown("Falls du wissen möchtest, wie diese App funktioniert, kannst du links im Menü auf die Seite **Methodik** klicken.")
    st.write("Dort wird erklärt, wie die App im Hintergrund arbeitet und wie die Risikoeinschätzung berechnet wird.")
## ende ChatGPT text






elif seite == "Eingaben":
    st.title("Deine Reisedaten")
    st.markdown("Damit die App eine persönliche Einschätzung geben kann, brauchen wir einige Angaben zu deiner Reise und zu deinem Gesundheitsprofil.")
    st.write("Die Informationen werden später verwendet, um die Luftqualität am gewählten Ort mit deinem Asthma-Level und deiner geplanten Aktivität zu verbinden.")

    st.divider()

    st.header("Eingaben")
    st.info("Je genauer die Angaben sind, desto besser kann die App später eine persönliche Einschätzung anzeigen.")

    ## column aufbau mit ChatGPT hergestellt
    col1, col2 = st.columns(2)

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

    with col2:
        st.subheader("Reiseangaben")
        st.caption("Diese Angaben beschreiben, wohin und wann du reisen möchtest.")

        ort = st.selectbox(
            "Wähle deinen Reiseort:", list(ORTE.keys()))

        reise_start = st.date_input("Wann beginnt deine Reise?")

        reise_ende = st.date_input(
            "Wann endet deine Reise?",
            min_value=reise_start)
## ende ChatGPT Bearbeitung

    if st.button("Eingaben speichern"):
        st.session_state["alter"] = alter
        st.session_state["asthma_level"] = asthma_level
        st.session_state["aktivitaet"] = aktivitaet
        st.session_state["ort"] = ort
        st.session_state["reise_start"] = reise_start
        st.session_state["reise_ende"] = reise_ende
        st.success("Deine Eingaben wurden gespeichert.")

    st.info("Wenn du alle Daten eingegeben hast, kannst du links im Menü auf Ergebnisse klicken, um deine Risikoeinschätzung zu sehen.")






elif seite == "Ergebnisse":
    st.title("Deine Ergebnisse")

    if "alter" in st.session_state:
        st.write("Hier siehst du die Angaben, die du auf der Eingabeseite gespeichert hast.")

        st.subheader("Gespeicherte Eingaben")

        st.write("Alter:", st.session_state["alter"])
        st.write("Asthma-Level:", st.session_state["asthma_level"])
        st.write("Aktivitätslevel:", st.session_state["aktivitaet"])
        st.write("Ort:", st.session_state["ort"])
        st.write("Reisebeginn:", st.session_state["reise_start"])
        st.write("Reiseende:", st.session_state["reise_ende"])

    else:
        st.warning("Bitte gehe zuerst auf die Seite Eingaben und speichere deine Angaben.")













else:
    st.header("Methodik")
    st.write("Hier wird erklärt, wie der Risikoscore berechnet wird.")
