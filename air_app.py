import streamlit as st
from api_call import fetch_air_quality
from datetime import date, timedelta
import pandas as pd
from weather_api import fetch_weather





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

MAX_FORECAST_TAGE = 14

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
    st.title("Deine Ergebnisse")

    if "alter" in st.session_state:
        st.write("Hier siehst du die Angaben, die du auf der Eingabeseite gespeichert hast.")

        st.subheader("Gespeicherte Eingaben")

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
        st.subheader("Wettervorhersage für dein Reise")

        ort_name = st.session_state["ort"]
        lon, lat = ORTE[ort_name]

##teilweise überarbeitet von ChatGPT:
        if st.button("Wetterdaten laden"):
            try:
                wetter = fetch_weather(
                    lat=lat,
                    lon=lon,
                    past_days=0,
                    forecast_days=MAX_FORECAST_TAGE
                )

                wetter_tabelle = wetter["daily"]

                wetter_tabelle["datum"] = pd.to_datetime(wetter_tabelle["date"]).dt.date

                reise_start = st.session_state["reise_start"]
                reise_ende = st.session_state["reise_ende"]

                wetter_reise = wetter_tabelle[
                    (wetter_tabelle["datum"] >= reise_start) &
                    (wetter_tabelle["datum"] <= reise_ende)
                    ]

                st.write("Wetterdaten für:", ort_name)

                durchschnitt_temp = wetter_reise["temperature_mean"].mean()
                durchschnitt_feuchtigkeit = wetter_reise["relative_humidity_mean"].mean()
                anzahl_tage = len(wetter_reise)

                col1, col2, col3 = st.columns(3)

                col1.metric("Reisetage", anzahl_tage)
##.1f heisst eine Nachkommastelle
                col2.metric("Ø Temperatur", f"{durchschnitt_temp:.1f} °C")

                col3.metric("Ø Luftfeuchtigkeit", f"{durchschnitt_feuchtigkeit:.1f} %")

                st.caption(
                    "Diese Wetterdaten werden später als Grundlage für die Vorhersage der Luftverschmutzung verwendet.")

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

            except Exception as fehler:
                st.error("Die Wetterdaten konnten nicht geladen werden.")
                st.write("Fehlermeldung:", fehler)
        else:
            st.info("Klicke auf den Button, um die Wettervorhersage für deinen Reisezeitraum zu laden.")

    else:
        st.warning("Bitte gehe zuerst auf die Seite Eingaben und speichere deine Angaben.")
##Ende ChatGPT Überarbeitung
















else:
    st.header("Methodik")
    st.write("Hier wird erklärt, wie der Risikoscore berechnet wird.")
## von Frieda
    st.title("About AirSense")

    st.write("""
    AirSense hilft Menschen mit Asthma zu erkennen, wann Aktivitäten im Freien ein erhöhtes Risiko darstellen können. 
    Die App kombiniert Daten zur Luftqualität, Wetterdaten und persönliche 
    Gesundheitsinformationen, um einen individuellen Risk-Score zu berechnen.
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
        Wenn Kinder (unter 18 Jahren) Triggern ausgesetzt sind, entzünden sich ihre Lungen und Atemwege leichter. 
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

        st.markdown("*Intermittierendes Asthma*")
        st.markdown("""
        - Tagesbeschwerden treten weniger als zweimal pro Woche auf, nächtliche Beschwerden weniger als zweimal pro Monat
        - Kaum bis keine Auswirkungen auf das tägliche Leben 
        """)

        st.markdown("*Schwach persistierendes Asthma*")
        st.markdown("""
            - Tagesbeschwerden treten 3–6 Mal pro Woche auf, nächtliche Beschwerden 3–4 Mal pro Monat
            - Leichte Einschränkungen bei den täglichen Aktivitäten sind möglich
            """)

        st.markdown("*Moderat persistierendes*")
        st.markdown("""
               - Symptome während dem Tag treten täglich auf, Symptome in der Nacht 5-mal oder öfter pro Monat
               - Alltägliche Aktivitäten sind etwas beeinträchtigt 
               """)

        st.markdown("*Schwer persistierendes Asthma*")
        st.markdown("""
               - Symptome während dem Tag treten den ganzen Tag über an, Symptome in der Nacht sind häufig
               - Starke Einschränkung der alltäglichen Aktivitäten
               """)

