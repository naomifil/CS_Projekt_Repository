def calculate_pm25_points(pm25):
    if pm25 <= 15:
        return 0
    elif pm25 <= 21:
        return 10
    elif pm25 <= 27:
        return 20
    elif pm25 <= 33:
        return 30
    elif pm25 <= 39:
        return 40
    elif pm25 <= 45:
        return 50
    elif pm25 <= 51:
        return 60
    elif pm25 <= 57:
        return 70
    elif pm25 <= 63:
        return 80
    elif pm25 <= 69:
        return 90
    else:
        return 100

#Fake values not sure how to connect it
pm25_value = 15
pm25_score = calculate_pm25_points(pm25_value)

def calculate_pm10_points(pm10):
   if pm10 <= 45:
        return 0
   elif pm10 <= 55.5:
        return 10
   elif pm10 <= 66:
        return 20
   elif pm10 <= 76.5:
        return 30
   elif pm10 <= 87:
        return 40
   elif pm10 <= 97.5:
        return 50
   elif pm10 <= 108:
       return 60
   elif pm10 <= 118.5:
       return 70
   elif pm10 <= 129:
       return 80
   elif pm10 <= 139.5:
       return 90
   else:
        return 100

#fake value
pm10_value = 45
pm10_score = calculate_pm10_points(pm10_value)

def calculate_o3_points(o3):
    if o3 <= 100:
        return 0
    elif o3 <= 106:
        return 10
    elif o3 <= 112:
        return 20
    elif o3 <= 118:
        return 30
    elif o3 <= 124:
        return 40
    elif o3 <= 130:
        return 50
    elif o3 <= 136:
        return 60
    elif o3 <= 142:
        return 70
    elif o3 <= 148:
        return 80
    elif o3 <= 154:
        return 90
    else:
        return 100

#fake value
o3_value = 100
o3_score = calculate_o3_points(o3_value)

def calculate_temperature_points(temperature):
    if temperature == 24:
        return 0

    # hotter than 24C
    if temperature > 24:
        if temperature <= 26:
            return 10
        elif temperature <= 28:
            return 20
        elif temperature <= 30:
            return 30
        elif temperature <= 32:
            return 40
        elif temperature <= 34:
            return 50
        elif temperature <= 36:
            return 60
        elif temperature <= 38:
            return 70
        elif temperature <= 40:
            return 80
        elif temperature <= 42:
            return 90
        else:
            return 100

    #colder than 24C
    else:
        if temperature >= 22:
            return 10
        elif temperature >= 20:
            return 20
        elif temperature >= 18:
            return 30
        elif temperature >= 16:
            return 40
        elif temperature >= 14:
            return 50
        elif temperature >= 12:
            return 60
        elif temperature >= 10:
            return 70
        elif temperature >= 8:
            return 80
        elif temperature >= 6:
            return 90
        else:
            return 100

temperature_value = 4
temperature_score = calculate_temperature_points(temperature_value)

def calculate_humidity_points(humidity):

    if humidity == 40:
        return 0

    #higher than 40
    if humidity > 40:
        if humidity <= 50:
            return 10
        elif humidity <= 54:
            return 20
        elif humidity <= 58:
            return 30
        elif humidity <= 62:
            return 40
        elif humidity <= 66:
            return 50
        elif humidity <= 70:
            return 60
        elif humidity <= 74:
            return 70
        elif humidity <= 78:
            return 80
        elif humidity <= 82:
            return 90
        else:
            return 100

    #lower than 40
    else:
        if humidity >= 30:
            return 10
        elif humidity >= 27:
            return 20
        elif humidity >= 24:
            return 30
        elif humidity >= 21:
            return 40
        elif humidity >= 18:
            return 50
        elif humidity >= 15:
            return 60
        elif humidity >= 12:
            return 70
        elif humidity >= 9:
            return 80
        elif humidity >= 6:
            return 90
        else:
            return 100

humidity_score = 10

#Environment score
environment_score = (
    pm25_score * 10 +
    o3_score * 8 +
    pm10_score * 5 +
    temperature_score * 3 +
    humidity_score * 1)

#personal factors
def get_age_factor(age):
    if age <= 14:
        return 3
    elif age < 65:
        return 1
    else:
        return 1.8

def get_activity_factor(activity):
    if activity == "indoor":
        return 1
    elif activity == "light_outdoor":
        return 1.5
    elif activity == "intense_outdoor":
        return 5
    else:
        return 1

def get_asthma_factor(asthma_level):
    if asthma_level == "intermittent":
        return 1
    elif asthma_level == "mild_persistent":
        return 1.5
    elif asthma_level == "moderate_persistent":
        return 2.5
    elif asthma_level == "severe_persistent":
        return 4
    else:
        return 1

age_value = 40
activity_value = "indoor"
asthma_level_value = "intermittent"

age_factor = get_age_factor(age_value)
activity_factor = get_activity_factor(activity_value)
asthma_factor = get_asthma_factor(asthma_level_value)

#RISK SCORE
risk_score = environment_score * age_factor * activity_factor * asthma_factor

def get_risk_level(score):

    if score <= 500:
        return "Sicher (Grün)", "Keine Gefahr. Optimale Bedingungen. Ideal für Sport und Aktivitäten im Freien für alle Gruppen"
    elif score <= 2500:
        return "Mässig (Gelb)", "Leichte Gefahr. Erste Reizungen bei empfindlichen Personen möglich. Moderate Aktivität im Freien ist okay."
    elif score <= 10000:
        return "Erhöht (Orange)", "Große Gefahr. Risikogruppen (Kinder/schweres Asthma) sollten intensive Anstrengung im Freien vermeiden. Medikation bereithalten."
    elif score <= 40000:
        return "Hoch (Rot)", "Sehr große Gefahr. Symptome sind sehr wahrscheinlich. Aktivitäten im Freien für alle Asthmatiker stark einschränken. Innenräume bevorzugen"
    else:
        return "Extrem (Violett)", "Extreme Gefahr. Akutes Risiko eines schweren Asthmaanfalls. Aufenthalt im Freien vermeiden, Fenster schließen, körperliche Ruhe."


level, message= get_risk_level(risk_score)

print(risk_score)
print(level)
print(message)



