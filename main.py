import datetime as dt
import requests

# Get API response
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
         
with open('api_key', 'r') as file:
    API_KEY = file.read()

CITY = "New York"

url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
response = requests.get(url).json()