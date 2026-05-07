import streamlit as st

st.title("About AirSense")

st.write("""
AirSense hilft Menschen mit Asthma zu erkennen, wann Aktivitäten im Freien ein erhöhtes Risiko darstellen können. 
Die App kombiniert Daten zur Luftqualität, Wetterdaten und persönliche 
Gesundheitsinformationen, um einen individuellen Risk-Score zu berechnen.
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

