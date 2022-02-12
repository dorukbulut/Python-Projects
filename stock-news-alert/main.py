import html
import requests
from twilio.rest import Client
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
stock_api_key = os.environ.get("STC_KEY")
stock_url = "https://www.alphavantage.co/query"

news_api_key = os.environ.get("NEWS_API")
news_api_url = "https://newsapi.org/v2/everything"

twilio_sid = os.environ.get("SID")
auth_token = os.environ.get("AUTH_TOKEN")

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api_key,

}
with requests.get(url=stock_url, params=stock_parameters) as response:
    response.raise_for_status()
    stock_data = response.json()

yesterday_closing_price = float(stock_data["Time Series (Daily)"]["2022-01-04"]["4. close"])
previous_day_closing_price = float(stock_data["Time Series (Daily)"]["2022-01-03"]["4. close"])

diff = yesterday_closing_price - previous_day_closing_price

percent = abs((diff / previous_day_closing_price) * 100)

if percent >= 5:

    news_parameters = {
        "q": COMPANY_NAME,
        "apiKey": news_api_key
    }

    with requests.get(url=news_api_url, params=news_parameters) as response:
        response.raise_for_status()
        news_data = [response.json()["articles"][news] for news in range(0, 3)]


    client = Client(twilio_sid, auth_token)

    for article in range(0, 3):
        message = client.messages.create(
            body=f"{COMPANY_NAME} %5\nTitle:\n{html.unescape(news_data[article]['title'])}\nDescription:{html.unescape(news_data[article]['description'])}",
            from_='NUM1',
            to='NUM2'
        )
        print(message.status)

