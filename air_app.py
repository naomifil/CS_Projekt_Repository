import streamlit as st

st.set_page_config(
    page_title="Luftqualitäts-App",
    layout="wide")


seite = st.sidebar.selectbox("Wähle eine Seite aus:",
    ["Startseite", "Eingaben", "Ergebnisse", "Methodik"])

if seite == "Startseite":
    st.title("Luftqualitäts-App für Reisen")
    st.header("Startseite")
    st.write("Willkommen in der Luftqualitäts-App. Diese App hilft dabei, das Risiko durch Luftverschmutzung während einer Reise einzuschätzen.")

    st.subheader("So benutzt du die App")
    ## folgender Text für seite (nicht der code) von ChatGPT erstellt
    st.markdown("""
    1. Gehe links im Menü auf **Eingaben**.
    2. Gib dort dein ***Alter***, dein ***Asthma-Level***, dein ***Aktivitätslevel*** und deine ***Reisedaten*** ein.
    3. Wähle den ***Ort*** aus, für den du das Risiko einschätzen möchtest.
    4. Gehe danach links im Menü auf **Ergebnisse**, um deinen Risikoscore und eine Empfehlung zu sehen.
    """)

    st.write("Die App ist eine einfache Entscheidungshilfe für Reisen und ersetzt keine medizinische Beratung.")

    st.subheader("Mehr über die App")

    st.markdown("Falls du wissen möchtest, wie diese App funktioniert, kannst du links im Menü auf die Seite **Methodik** klicken.")
    st.write("Dort wird erklärt, wie die App im Hintergrund arbeitet und wie die Risikoeinschätzung berechnet wird.")
## ende ChatGPT text

elif seite == "Eingaben":
    st.header("Eingaben")
    st.write("Hier werden Alter, Asthma-Level, Aktivitätslevel, Reisedatum und Ort eingegeben.")

elif seite == "Ergebnisse":
    st.header("Ergebnisse")
    st.write("Hier werden der Risikoscore und die Empfehlung angezeigt.")

else:
    st.header("Methodik")
    st.write("Hier wird erklärt, wie der Risikoscore berechnet wird.")
