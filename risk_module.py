
def calculate_pm25(pm25):
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

def calculate_pm10(pm10):
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


def calculate_o3(o3):
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

def calculate_temperature(temperature):
    if temperature == 24:
        return 0

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


def calculate_humidity(humidity):
    if humidity == 40:
        return 0

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


def get_alter_level(alter):
    if alter <= 1:
        return 3.5
    elif alter <= 3:
        return 2.5
    elif alter <= 12:
        return 1.7
    elif alter < 65:
        return 1.0
    elif alter <= 75:
        return 1.7
    else:
        return 3.5

def get_activitaet_level(aktivitaet):
    if aktivitaet == "Nicht aktiv":
        return 1
    elif aktivitaet == "Aktiv":
        return 1.5
    elif aktivitaet == "Sehr aktiv":
        return 3
    else:
        return 1

def get_asthma_level(asthma_level):
    if asthma_level == "Kein Asthma":
        return 1
    elif asthma_level == "Leicht":
        return 1.5
    elif asthma_level == "Mittel":
        return 2.5
    elif asthma_level == "Stark":
        return 4
    else:
        return 1

def calculate_total_risk(pm25, pm10, o3, temperature, humidity, alter, aktivitaet, asthma_level):
    pm25_score = calculate_pm25(pm25)
    pm10_score = calculate_pm10(pm10)
    o3_score = calculate_o3(o3)

    temperature_score = calculate_temperature(temperature)
    humidity_score = calculate_humidity(humidity)

    alter_factor = get_alter_level(alter)
    aktivitaet_factor = get_activitaet_level(aktivitaet)
    asthma_factor = get_asthma_level(asthma_level)

    umwelt_score = (
            pm25_score * 10 +
            o3_score * 8 +
            pm10_score * 5 +
            temperature_score * 1 +
            humidity_score * 1
    )

    risiko_score = umwelt_score * alter_factor * aktivitaet_factor * asthma_factor

    if risiko_score <= 300:
        risiko_level = "Sicher"
        farbe = "Grün"
        empfehlung = "Für dich wirkt das Risiko aktuell niedrig. Du kannst deine geplanten Aktivitäten grundsätzlich normal durchführen, solltest aber trotzdem auf dein eigenes Befinden achten."

    elif risiko_score <= 1500:
        risiko_level = "Mässig"
        farbe = "Gelb"
        empfehlung = "Für dich besteht ein leicht erhöhtes Risiko. Du kannst nach draussen gehen, solltest aber starke Anstrengung reduzieren und auf mögliche Symptome wie Husten, Engegefühl oder Atemprobleme achten."

    elif risiko_score <= 6000:
        risiko_level = "Erhöht"
        farbe = "Orange"
        empfehlung = "Für dich ist das Risiko erhöht. Plane lieber ruhigere Aktivitäten ein, vermeide intensive Belastung im Freien und halte deine Medikamente oder dein Inhalationsgerät bereit."

    elif risiko_score <= 24000:
        risiko_level = "Hoch"
        farbe = "Rot"
        empfehlung = "Für dich ist das Risiko hoch. Du solltest längere Aufenthalte und anstrengende Aktivitäten im Freien möglichst vermeiden. Wenn du Beschwerden spürst, bleibe drinnen und nutze deine Medikamente wie empfohlen."

    else:
        risiko_level = "Extrem"
        farbe = "Violett"
        empfehlung = "Für dich ist das Risiko sehr hoch. Vermeide Aufenthalt und körperliche Anstrengung im Freien möglichst vollständig. Bleibe wenn möglich in Innenräumen und achte besonders auf Atembeschwerden."

    return risiko_score, risiko_level, farbe, empfehlung

