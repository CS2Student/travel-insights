import datetime as dt
import requests

# Get API response
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

with open('api_key', 'r') as file:
    API_KEY = file.read()

CITY = "New York"

url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
response = requests.get(url).json()


# Temperature conversion function
def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit


# Parse necessary values
temp_kelvin = response['main']['temp']
temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
feels_like_kelvin = response['main']['feels_like']
feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(
    feels_like_kelvin)
wind_speed = response['wind']['speed']
humidity = response['main']['humidity']
description = response['weather'][0]['description']
sunrise_time = dt.datetime.utcfromtimestamp(
    response['sys']['sunrise'] + response['timezone'])
sunset_time = dt.datetime.utcfromtimestamp(
    response['sys']['sunset'] + response['timezone'])
