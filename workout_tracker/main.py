import os
from datetime import datetime


import requests

# MY INFO
GENDER = "male"
MY_WEİGHT = 70
MY_HEİGHT = 180.0
MY_AGE = 20

# Nutri

APP_ID = os.environ.get("APP_ID")

API_KEY = os.environ.get("API_KEY")
nutri_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
TOKEN = os.environ.get("TOKEN")
print(TOKEN)

exercise_text = input("Tell me which exercise you did today :")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": MY_WEİGHT,
    "height_cm": MY_HEİGHT,
    "age": MY_AGE
}

response = requests.post(url=nutri_endpoint, json=params, headers=headers)
response.raise_for_status()

exercise_data = response.json()

sheety_endpoint = "https://api.sheety.co/8e899559bfcfd3f3f3c16ac7cad99673/myWorkouts/workouts"
sheety_headers = {
    "Authorization": "Bearer XXXXX"

}

today = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in exercise_data["exercises"]:
    row_config = {
        "workout": {
            "date": today,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": str(exercise["duration_min"]),
            "calories": exercise["nf_calories"],
        }
    }

    sheet_response = requests.post(url=sheety_endpoint, json=row_config, headers=sheety_headers)
    sheet_response.raise_for_status()

    print(sheet_response.text)
