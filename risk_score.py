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
pm25_value = 20
pm25_score = calculate_pm25_points(pm25_value)


print("PM2.5 points:", pm25_score)

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
pm10_value = 110
pm10_score = calculate_pm10_points(pm10_value)

print("pm10 points:", pm10_score)

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
o3_value = 136.1
o3_score = calculate_o3_points(o3_value)

print("o3 points:", o3_score)

def calculate_temperature_points(temperature):
    if temperature = 24:
        return 0

    # hotter than 24C
    if temperature > 24:
        if temperature <= 26:
            return 10
        elif temperature <= 28:
            return 20
        elif temperature <= 30:
            return 30

# CONTINUE
