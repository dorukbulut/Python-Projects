import requests
from twilio.rest import Client
import os
api_key = os.environ.get("API_KEY") 
accound_sid = os.environ.get("ACC_SID")
auth_token = os.environ.get("AUTH_TOKEN")


parameters = {
    "lat": 40.383560,
    "lon": -5.766050,
    "exclude": "current,minutely,daily",
    "appid": api_key

}

response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()

weather_data = response.json()

next_12_hours = [weather_data["hourly"][i]["weather"][0]["id"] for i in range(0,12)]

for id in next_12_hours:
    if  id < 700:
        client = Client(accound_sid,auth_token)
        message = client.messages.create(body="It's going to rain bring your umbrella!",
                                         from_= "twilio_num",
                                         to="your_phone_num"
                                         )
        break


print(message.status)
