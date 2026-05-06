import streamlit as st
import pandas as pd

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
    - ihr persönliches Risiko zu bewerten (jeder reagiert unterschiedlich)
    - Wetter, Luftverschmutzung und Gesundheit miteinander zu verbinden
    """)

with st.expander("**Die Lösung**"):

    st.write("Das Ziel unseres Projekts ist es, Menschen mit Asthma dabei zu helfen, bessere und sicherere Entscheidungen im Alltag zu treffen.")

    st.write("Unsere App:")

    st.write("""
    - sammelt Echtzeitdaten zur Luftqualität und zum Wetter
    - kombiniert diese mit dem Gesundheitsprofil des Nutzers
    - berechnet daraus einen personalisierten Asthma Risk-Score
    - stellt das Ergebnis klar und verständlich dar
    """)

st.divider()

st.header("Einflussfaktoren auf den Risk-Score")

st.write("""Der Risk-Score wird aus einer Kombination von Umweltfaktoren und persönlichen Faktoren berechnet. Dazu gehören:""")

#Umweltfaktoren
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

    st.write("Jeder Faktor wird in einen Punktwert zwischen 0 und 100 umgerechnet, je nachdem, wie schädlich der gemessene Wert ist.")

    st.write("**Gewichtung**")
    st.write("Nicht alle Faktoren sind gleich wichtig:")
    st.write("""
    - PM2,5 → stärkster Einfluss (Faktor von 10)
    - Ozon → hoher Einfluss (Faktor von 8)
    - PM10 → mittlerer Einfluss (Faktor von 5)
    - Temperatur → geringerer Einfluss (Faktor von 3)
    - Luftfeuchtigkeit → geringster Einfluss (Faktor von 1)
    """)

    #WHERE IS THE INFO THAT SAYS WHY SOME ARE WORSE

with st.expander("**Persönliche Faktoren**"):

    st.write("Der Wert wird anhand folgender Faktoren angepasst:")

    st.write("**Alter**")
    st.write("""
    - Kind → 0-14 (Faktor von 3)
    - Erwachsener → 15-65 (Faktor von 1)
    - Senioren → > 65 (Faktor von 1.8)
    """)

    st.write("**Aktivität**")
    st.write("""
    - Innenraum (Faktor von 1)
    - Draussen leichte Aktivität (Faktor von 1.5)
    - Draussen intensive Aktivität (Faktor von 5) 
    """)

    st.write("**Asthmaschweregrade**")
    st.write("""
    - Intermittierend (Faktor von 1)
    - Mild persistent (Faktor von 1.5)
    - Moderat persistent (Faktor von 2.5)
    - Schwer persistent (Faktor von 4)
    """)

with st.expander("**Endergebnis und Risikoschwellwerte**"):
    st.write(
        "Alle Punkte werden mit ihren Gewichten multipliziert und zu einer Gesamtrisikobewertung zusammengerechnet.")


    st.subheader("Sicher", divider="green")
    st.write(":green-background[**0-500 Punkte**]")
    st.write(":green-background[Keine Gefahr. Optimale Bedingungen. Ideal für Sport und Aktivitäten im Freien für alle Gruppen]")

    st.subheader("Mässig", divider="yellow")
    st.write(":yellow-background[**501-2500 Punkte**]")
    st.write(":yellow-background[Leichte Gefahr. Erste Reizungen bei empfindlichen Personen möglich. Moderate Aktivität im Freien ist okay.]")

    st.subheader("Erhöht", divider="orange")
    st.write(":orange-background[**2501-10000 Punkte**]")
    st.write(":orange-background[Grosse Gefahr. Risikogruppen (Kinder/schweres Asthma) sollten intensive Anstrengung im Freien vermeiden. Medikation bereithalten.]")

    st.subheader("Hoch", divider="red")
    st.write(":red-background[**10001-40000 Punkte**]")
    st.write(":red-background[Sehr grosse Gefahr. Symptome sind sehr wahrscheinlich. Aktivitäten im Freien für alle Asthmatiker stark einschränken. Innenräume bevorzugen.]")

    st.subheader("Extrem", divider="violet")
    st.write(":violet-background[**mehr als 40000 Punkte**]")
    st.write(":violet-background[Extreme Gefahr. Akutes Risiko eines schweren Asthmaanfalls. Aufenthalt im Freien vermeiden, Fenster schließen, körperliche Ruhe.]")


with st.expander(":orange[**⚠ User Warning ⚠**]"):
    st.write("Diese App ist kein medizinisches Hilfsmittel.")
    st.write("""
   - Wir sind keine Ärzte.
   - Der Risikowert ist eine Schätzung auf der Grundlage der verfügbaren Daten.
   - Die App ersetzt keine professionelle medizinische Beratung.
   - Bei Symptomen sollten Nutzer immer einen Arzt konsultieren.
   """)

st.divider()

st.header("Quellen")
with st.expander("Einflussfaktoren auf den Risk-Score"):
    st.write("PM2.5: bla")