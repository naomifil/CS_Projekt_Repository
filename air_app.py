import streamlit as st
from api_call import fetch_air_quality
from datetime import date, timedelta
import pandas as pd
from weather_api import fetch_weather
from ml_model_db import train_model_for_city, predict_multiple_days
from risk_module import calculate_total_risk





##Dictionary code gemacht von ChatGPT
ORTE = {
    "Zürich": (8.5417, 47.3769),
    "Paris": (2.3522, 48.8566),
    "Berlin": (13.4050, 52.5200),
    "London": (-0.1278, 51.5074),
    "Frankfurt": (8.6821, 50.1109),
    "Brüssel": (4.3517, 50.8503),
    "Stockholm": (18.0686, 59.3293)}
## für das ML modell
ORT_IDS = {
    "Paris": "1",
    "Zürich": "2",
    "Berlin": "3",
    "London": "4",
    "Frankfurt": "5",
    "Brüssel": "6",
    "Stockholm": "7"}

PARAMETER = ["pm25", "pm10", "o3"]
##Ende ChatGPT

MAX_FORECAST_TAGE = 14

MAX_RISIKO_SCORE = 105000

##Funktion mit einzelnen farben von ChatGPT gemacht
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

##damit das ML nicht bei jedem rerun neu trainiert wird, merkt sich streamlit das trainierte modell durch cache funktion
@st.cache_resource
def lade_ml_modell(location_id):
    model, mae, predictions = train_model_for_city(location_id)
    return model, mae

@st.cache_data(ttl=300)
def lade_wetterdaten(lat, lon, forecast_tage):
    wetter = fetch_weather(
        lat=lat,
        lon=lon,
        past_days=0,
        forecast_days=forecast_tage)
    return wetter

st.set_page_config(
    page_title="AirSense",
    layout="wide")

st.sidebar.title("Menü")
seite = st.sidebar.selectbox("Wähle eine Seite aus:",
    ["Startseite", "Eingaben", "Ergebnisse", "Methodik"])





if seite == "Startseite":
    st.title("AirSense: eine Luftqualitäts-App für Reisen")
    st.header("Startseite")
    st.markdown(
        "Diese App hilft dir dabei, **vor einer Reise** nochmals zu überprüfen, "
        "wie hoch das mögliche Risiko durch Luftverschmutzung am **Reiseziel** sein könnte. "
        "So kannst du deine Reiseplanung besser einschätzen und entscheiden, "
        "ob du deine Aktivitäten anpassen solltest.")



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
    st.write("Hier kannst du deine Daten eingeben.")

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

        heute = date.today()
        max_datum = heute + timedelta(days=MAX_FORECAST_TAGE)

        ort = st.selectbox(
            "Wähle deinen Reiseort:", list(ORTE.keys()))

        reise_start = st.date_input("Wann beginnt deine Reise?", min_value=heute, max_value=max_datum)

        reise_ende = st.date_input(
            "Wann endet deine Reise?",
            min_value=reise_start, max_value=max_datum)

        st.caption("Hinweis: Die App erlaubt aktuell nur Reisedaten innerhalb der nächsten 14 Tage, weil die Wettervorhersage nur für einen begrenzten Zeitraum verfügbar ist.")
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
    st.write("Hier kannst du dir deine Ergebnisse anschauen.")
    st.title("Deine persönliche Risikoeinschätzung")

    if "alter" in st.session_state:

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

        if st.button("Ergebnisse laden"):
            try:
                wetter = lade_wetterdaten(
                    lat=lat,
                    lon=lon,
                    forecast_tage=MAX_FORECAST_TAGE
                )

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

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Höchster Risiko-Score", round(schlimmster_tag["risiko_score"], 2))
                    st.caption("Der maximal mögliche Risiko-Score ist 105'000")

                with col2:
                    st.metric("Kritischster Tag", schlimmster_tag["datum"].strftime("%d.%m.%Y"))

                with col3:
                    st.metric("Risikostufe", schlimmster_tag["risiko_level"])

                st.subheader("Risikoverlauf während der Reise")

                risiko_graph = vorhersage[["datum", "risiko_score"]].copy()
                risiko_graph = risiko_graph.set_index("datum")

                st.line_chart(risiko_graph)

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

                st.divider()
                st.subheader("Vorhergesagte Luftverschmutzung")

                st.write("Das Modell schätzt aus den Wetterdaten die Luftverschmutzung für deine Reisetage.")
                st.caption(f"Durchschnittlicher Modellfehler im Test: {mae:.2f}")

                st.dataframe(
                    vorhersage[["datum", "pm25", "pm10", "o3"]],
                    use_container_width=True,
                    hide_index=True
                )

                st.subheader("Entwicklung der vorhergesagten Schadstoffe")

                schadstoff_graph = vorhersage[["datum", "pm25", "pm10", "o3"]].copy()
                schadstoff_graph = schadstoff_graph.set_index("datum")

                st.line_chart(schadstoff_graph)

                st.divider()
                st.subheader("Wettervorhersage für deine Reise")

                st.write("Wetterdaten für:", ort_name)

                durchschnitt_temp = wetter_reise["temperature_mean"].mean()
                durchschnitt_feuchtigkeit = wetter_reise["relative_humidity_mean"].mean()
                anzahl_tage = len(wetter_reise)

                col1, col2, col3 = st.columns(3)

                col1.metric("Reisetage", anzahl_tage)

                # .1f heisst eine Nachkommastelle
                col2.metric("Ø Temperatur", f"{durchschnitt_temp:.1f} °C")

                col3.metric("Ø Luftfeuchtigkeit", f"{durchschnitt_feuchtigkeit:.1f} %")

                st.caption(
                    "Diese Wetterdaten werden später als Grundlage für die Vorhersage der Luftverschmutzung verwendet."
                )

                st.subheader("Temperatur während der Reise")

                temperatur_graph = wetter_reise[["datum", "temperature_mean"]].copy()
                temperatur_graph = temperatur_graph.set_index("datum")

                st.line_chart(temperatur_graph)

                st.subheader("Relative Luftfeuchtigkeit während der Reise")

                feuchtigkeit_graph = wetter_reise[["datum", "relative_humidity_mean"]].copy()
                feuchtigkeit_graph = feuchtigkeit_graph.set_index("datum")

                st.line_chart(feuchtigkeit_graph)

                with st.expander("Wetterdaten als Tabelle anzeigen"):
                    st.dataframe(
                        wetter_reise[["datum", "temperature_mean", "relative_humidity_mean"]],
                        use_container_width=True,
                        hide_index=True
                    )

            except ValueError as fehler:
                st.error("Für diesen Ort gibt es aktuell nicht genügend Daten für das ML-Modell.")
                st.write("Bitte versuche es mit einem anderen Ort, zum Beispiel Zürich oder Paris.")
                st.caption(f"Technische Fehlermeldung: {fehler}")

            except Exception as fehler:
                st.error("❌ Die Ergebnisse konnten nicht berechnet werden.")
                st.write("Fehlermeldung:", fehler)

        else:
            st.info(
                "Klicke auf den Button, um Wetterdaten, Luftverschmutzung und dein persönliches Risiko zu berechnen.")

    else:
        st.warning("Bitte gehe zuerst auf die Seite Eingaben und speichere deine Angaben.")
##Ende ChatGPT Überarbeitung
















else:

    st.write("Hier wird erklärt, wie der Risikoscore berechnet wird.")
## von Frieda
    st.title("About AirSense")

    st.write("""
    AirSense hilft Menschen mit Asthma zu erkennen, wann Aktivitäten im Freien ein erhöhtes Risiko darstellen können. 
    Die App kombiniert Daten zur Luftqualität, Wetterdaten und persönliche 
    Gesundheitsinformationen, um einen individuellen Risk-Score zu berechnen.
    """)

    with st.expander("**Das Problem**"):

        st.write("Menschen mit Asthma haben oft Schwierigkeiten damit:")

        st.write("""
        - Luftqualitätsdaten zu verstehen
        - Zu wissen, wann es sicher ist, nach draussen zu gehen
        - Ihr persönliches Risiko zu bewerten (jeder reagiert unterschiedlich)
        - Wetter, Luftverschmutzung und Gesundheit miteinander zu verbinden
        """)

    with st.expander("**Die Lösung**"):

        st.write(
            "Das Ziel unseres Projekts ist es, Menschen mit Asthma dabei zu helfen, bessere und sicherere Entscheidungen im Alltag zu treffen.")

        st.write("Unsere App:")

        st.write("""
        - sammelt Echtzeitdaten zur Luftqualität und zum Wetter
        - kombiniert diese mit dem Gesundheitsprofil des Nutzers
        - berechnet daraus einen personalisierten Asthma Risk-Score
        - stellt das Ergebnis klar und verständlich dar
        """)

    st.divider()

    st.header("Einflussfaktoren auf den Risk-Score")

    st.write(
        """Der Risk-Score wird aus einer Kombination von Umweltfaktoren und persönlichen Faktoren berechnet. Dazu gehören:""")

    # Umweltfaktoren
    st.subheader("Umweltfaktoren")

    st.markdown("##### Luftverschmutzung")
    st.write("""
    Luftverschmutzung kann das Risiko erhöhen, an Asthma zu erkranken, oder die Symptome verschlimmern,
    wenn man bereits an Asthma leidet.
    """)

    with st.expander("**PM2.5 und PM10**"):
        st.write("""
        PM steht für „Particulate Matter“ (Feinstaub), diese Partikel können aus vielen verschiedenen Chemikalien bestehen.
        Die meisten davon entstehen bereits in der Atmosphäre durch Reaktionen von Schadstoffen, die aus Kraftwerken,
        Autos und anderen Quellen stammen. Einige kommen direkt von Quellen wie Bränden oder Baustellen.
        Feinstaub kann eingeatmet werden und schwere Gesundheitsprobleme verursachen. 
        """)

        st.markdown("*PM2.5*")
        st.write("""
        Hierbei handelt es sich um Feinstaubpartikel mit einem Durchmesser von 2,5 Mikrometern oder weniger. 
        Diese stellen ein höheres Gesundheitsrisiko dar als PM10. Beispiele für PM2,5 sind Verbrennungspartikel, Rauch und Russ.
        """)

        st.markdown("*PM10*")
        st.write("""
        Dies sind Feinstaubpartikel mit einem Durchmesser von 10 Mikrometern oder weniger. 
        Obwohl sie ein geringeres Gesundheitsrisiko darstellen als PM2,5, können sie dennoch gefährlich sein, 
        da sie ebenfalls tief in die Lunge oder sogar in den Blutkreislauf gelangen können. Beispiele für PM10 sind Staub, Pollen usw.
        """)

        st.write("""
        Bei Menschen mit Asthma können diese Feinstaubpartikel die Atemwege reizen und Asthmasymptome verschlimmern.
        """)

    with st.expander("**O3**"):

        st.write("""
        Ozon ist ein gasförmiger Luftschadstoff, der in Bodennähe gesundheitsschädlich wird. Es ist ein Hauptbestandteil 
        von Smog und tritt häufig in Städten mit hohem Autoverkehr und hohen Emissionen aus fossilen Brennstoffen auf.
        Bodennahes Ozon entsteht durch chemische Reaktionen zwischen Schadstoffen (z. B. Fahrzeugabgasen), Sonnenlicht und Wärme.
        Ozon reizt die Atemwege stark und kann Asthma sowie andere Lungenerkrankungen auslösen oder verschlimmern.
        """)

    st.markdown("##### Wetterbedingungen")

    with st.expander("**Temperatur**"):
        st.write("""
        Kalte und heisse Temperaturen können Asthmasymptome auslösen. Kalte, trockene Luft kann die Atemwege irritieren, 
        wodurch sich diese zusammenziehen und Husten sowie Atemnot verursacht werden. Hohe Hitze kann Asthma ebenfalls verschlimmern, 
        indem sie die Luftverschmutzung und die Konzentration von Allergenen erhöht, die die Lunge reizen.
        """)

    with st.expander("**Luftfeuchtigkeit**"):
        st.write("""
        Auch Luftfeuchtigkeit kann Asthma beeinflussen. Feuchte Luft ist schwerer und begünstigt Allergene wie Schimmel und Staubmilben.
        Zudem kann sie die Luftverschmutzung verschlimmern und Symptome auslösen. Sehr trockene Luft kann auch die Atemwege reizen und zu Atembeschwerden führen.
        """)

    st.subheader("Persönliche Faktoren")
    st.write("""
    Persönliche Faktoren spielen eine wichtige Rolle dabei, wie stark sich Umweltbedingungen auf Menschen mit Asthma auswirken. 
    Jeder Mensch reagiert je nach Gesundheitszustand und Verhalten unterschiedlich.""")

    with st.expander("**Alter**"):
        st.write("""
        Das Alter beeinflusst, wie empfindlich eine Person auf Luftverschmutzung und Wetterbedingungen reagiert.
        Wenn Kinder (unter 14 Jahren) Triggern ausgesetzt sind, entzünden sich ihre Lungen und Atemwege leichter. 
        Ältere Erwachsene (ab 65 Jahren) reagieren empfindlicher auf Asthmaauslöser, da die Lungenfunktion mit zunehmendem Alter abnimmt 
        und die Symptome schlimmer sind oder schwieriger zu behandeln sein können.
        """)

    with st.expander("**Aktivitätsniveau**"):
        st.write("""
        Körperliche Aktivität erhöht die Frequenz und Tiefe der Atmung, was zu einer höheren Aufnahme von Luftschadstoffen führt, die die Atemwege reizen können. 
        Dazu kann bei manchen Menschen körperliche Betätigung selbst Asthmasymptome auslösen, die durch Schadstoffe noch verschlimmert werden können. 
        """)

    with st.expander("**Asthma-Schweregrade**"):
        st.write("""
        Um ihren Risikowert weiter zu personalisieren, können Nutzer ihre Asthma-Stufe angeben. 
        Unsere App unterscheidet zwischen den vier Stufen, die von den meisten Ärzten und Forschern verwendet werden. 
        """)

        st.markdown("*Kein bis sehr leicht persistierendes Asthma*")
        st.markdown("""
        - Tagesbeschwerden treten weniger als zweimal pro Woche auf, nächtliche Beschwerden weniger als zweimal pro Monat
        - Kaum bis keine Auswirkungen auf das tägliche Leben 
        """)

        st.markdown("*Schwach persistierendes Asthma*")
        st.markdown("""
            - Tagesbeschwerden treten 3–6 Mal pro Woche auf, nächtliche Beschwerden 3–4 Mal pro Monat
            - Leichte Einschränkungen bei den täglichen Aktivitäten sind möglich
            """)

        st.markdown("*Moderat persistierendes Asthma*")
        st.markdown("""
               - Symptome während dem Tag treten täglich auf, Symptome in der Nacht 5-mal oder öfter pro Monat
               - Alltägliche Aktivitäten sind etwas beeinträchtigt 
               """)

        st.markdown("*Schwer persistierendes Asthma*")
        st.markdown("""
               - Symptome während dem Tag treten den ganzen Tag über an, Symptome in der Nacht sind häufig
               - Starke Einschränkung der alltäglichen Aktivitäten
               """)

    st.divider()

    st.header("Berechnung des Risk-Scores")
    with st.expander("**Umweltfaktoren**"):

        st.write("""
        - PM2.5
        - PM10 
        - O3
        - Temperatur
        - Luftfeuchtigkeit
        """)

        st.write(
            "Jeder Faktor wird in einen Punktwert zwischen 0 und 100 umgerechnet, je nachdem, wie schädlich der gemessene Wert ist.")

        st.write("**Gewichtung**")
        st.write("Nicht alle Faktoren sind gleich wichtig:")
        st.write("""
        - PM2,5 → stärkster Einfluss (Faktor von 10)
        - Ozon → hoher Einfluss (Faktor von 8)
        - PM10 → mittlerer Einfluss (Faktor von 5)
        - Temperatur → geringerer Einfluss (Faktor von 1)
        - Luftfeuchtigkeit → geringster Einfluss (Faktor von 1)
        """)



    with st.expander("**Persönliche Faktoren**"):

        st.write("Der Wert wird anhand folgender Faktoren angepasst:")

        st.write("**Alter**")
        st.write("""
        - Kleinkinder bis 1 Jahr → Faktor 3.5
        - Kinder von 2 bis 3 Jahren → Faktor 2.5
        - Kinder von 4 bis 12 Jahren → Faktor 1.7
        - Erwachsene von 13 bis 64 Jahren → Faktor 1.0
        - Ältere Personen von 65 bis 75 Jahren → Faktor 1.7
        - Personen über 75 Jahre → Faktor 3.5
        """)

        st.write("**Aktivität**")
        st.write("""
        - Nicht aktiv → Faktor 1.0
        - Aktiv → Faktor 1.5
        - Sehr aktiv → Faktor 3.0
        """)

        st.write("**Asthmaschweregrade**")
        st.write("""
        - Intermittierend (Faktor von 1.0)
        - Mild persistent (Faktor von 1.5)
        - Moderat persistent (Faktor von 2.5)
        - Schwer persistent (Faktor von 4.0)
        """)

    with st.expander("**Endergebnis und Risikoschwellwerte**"):
        st.write(
            "Alle Punkte werden mit ihren Gewichten multipliziert und zu einer Gesamtrisikobewertung zusammengerechnet.")

        st.subheader("Sicher", divider="green")
        st.write(":green-background[**0-300 Punkte**]")
        st.write(
            ":green-background[Keine Gefahr. Optimale Bedingungen. Ideal für Sport und Aktivitäten im Freien für alle Gruppen]")

        st.subheader("Mässig", divider="yellow")
        st.write(":yellow-background[**301-1500 Punkte**]")
        st.write(
            ":yellow-background[Leichte Gefahr. Erste Reizungen bei empfindlichen Personen möglich. Moderate Aktivität im Freien ist okay.]")

        st.subheader("Erhöht", divider="orange")
        st.write(":orange-background[**1501-6000 Punkte**]")
        st.write(
            ":orange-background[Grosse Gefahr. Risikogruppen (Kinder/schweres Asthma) sollten intensive Anstrengung im Freien vermeiden. Medikation bereithalten.]")

        st.subheader("Hoch", divider="red")
        st.write(":red-background[**6001-24000 Punkte**]")
        st.write(
            ":red-background[Sehr grosse Gefahr. Symptome sind sehr wahrscheinlich. Aktivitäten im Freien für alle Asthmatiker stark einschränken. Innenräume bevorzugen.]")

        st.subheader("Extrem", divider="violet")
        st.write(":violet-background[**mehr als 24000 Punkte**]")
        st.write(
            ":violet-background[Extreme Gefahr. Akutes Risiko eines schweren Asthmaanfalls. Aufenthalt im Freien vermeiden, Fenster schließen, körperliche Ruhe.]")

    with st.expander(":orange[**⚠ User Warning ⚠**]"):
        st.write("Diese App ist kein medizinisches Hilfsmittel.")
        st.write("""
       - Wir sind keine Ärzte.
       - Der Risikowert ist eine Schätzung auf der Grundlage der verfügbaren Daten.
       - Die App ersetzt keine professionelle medizinische Beratung.
       - Bei Symptomen sollten Nutzer immer einen Arzt konsultieren.
       """)

    st.divider()

    st.header("Zusätzliche Informationen")
    with st.expander("**Quellen**"):
        st.write("""
        *Air Pollution and Asthma | AAFA.org.* (2025, September 4). Asthma and Allergy Foundation of America.  
        https://aafa.org/asthma/asthma-triggers-causes/air-pollution-smog-asthma/

        American Lung Association. (n.d.). *Why is my asthma worse in the winter?*  
        https://www.lung.org/blog/cold-weather-asthma

        *Asthma in older adults | AAFA.org.* (2024, October 11). Asthma and Allergy Foundation of America.  
        https://aafa.org/asthma/living-with-asthma/asthma-in-older-adults/

        *Childhood asthma - Symptoms & causes - Mayo Clinic.* (2025, September 20). Mayo Clinic.  
        https://www.mayoclinic.org/diseases-conditions/childhood-asthma/symptoms-causes/syc-20351507

        Global Initiative for Asthma. (2025). *Global Strategy for Asthma Management and Prevention* [Report].

        Han, A., Deng, S., Yu, J., Zhang, Y., Jalaludin, B., & Huang, C. (2022). *Asthma triggered by extreme temperatures: From epidemiological evidence to biological plausibility.* Environmental Research, 216(Pt 2), 114489.  
        https://doi.org/10.1016/j.envres.2022.114489

        *How Severe is My Asthma: Classifying Asthma Severity.* (2021, May 20). Allergy & Asthma Network.  
        https://allergyasthmanetwork.org/news/how-severe-is-my-asthma/#intermittent

        Huang, J., Yang, X., Fan, F., Hu, Y., Wang, X., Zhu, S., Ren, G., & Wang, G. (2021). *Outdoor air pollution and the risk of asthma exacerbations in single lag0 and lag1 exposure patterns: a systematic review and meta-analysis.* Journal of Asthma, 59(11), 2322–2339.  
        https://doi.org/10.1080/02770903.2021.2008429

        Koehle, M. S. (2024). *Physiological impacts of atmospheric pollution: Effects of environmental air pollution on exercise.* Physiological Reports, 12(7), e16005.  
        https://doi.org/10.14814/phy2.16005

        MSD Manual. (2026, May 7). *Table: Klassifikation der Asthma-Schweregrads*-MSD Manual Profi-Ausgabe. MSD Manual Profi-Ausgabe.  
        https://www.msdmanuals.com/de/profi/multimedia/table/klassifikation-der-asthma-schweregrads

        *Particulate Matter (PM) Basics | US EPA.* (2025, May 30). US EPA.  
        https://www.epa.gov/pm-pollution/particulate-matter-pm-basics

        *Summer asthma and warm weather.* (n.d.). Allergy & Asthma Network.  
        https://allergyasthmanetwork.org/news/summer-asthma-and-warm-weather

        *Weather triggers asthma | AAFA.org.* (2024, August 20). Asthma and Allergy Foundation of America.  
        https://aafa.org/asthma/asthma-triggers-causes/weather-triggers-asthma/

        Weltgesundheitsorganisation, & Organization, W. H. (2021). *WHO global air quality guidelines: particulate matter (PM2.5 and PM10), ozone, nitrogen dioxide, sulfur dioxide and carbon monoxide.* World Health Organization.

        *What is exercise induced asthma? | AAFA.org.* (2024, August 5). Asthma and Allergy Foundation of America.  
        https://aafa.org/asthma/asthma-triggers-causes/exercise-induced-asthma/
        """)

    with st.expander("**Hilfsmittel**"):
        st.write("Deepl Translate")