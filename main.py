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


# Recommendation Functions

# Temperature Recommendation
def temp_rec(temp_celsius):
    temp_celsius = round(float(temp_celsius), 2)
    if temp_celsius < 10:
        return "JACKET, SWEATPANTS, WINTER SHOES"
    elif temp_celsius < 20:
        return "SWEATER, SWEATPANTS, CASUAL SHOES"
    elif temp_celsius < 35:
        return "SHORTS, RUNNING SHOES"
    elif temp_celsius < 40:
        return "HEAT WAVE"


# Wind Speed Recommendation
def wind_rec(wind_speed):
    if wind_speed < 5:
        return "It's calm outside"
    elif wind_speed < 10:
        return "There is a moderate breeze outside"
    elif wind_speed < 20:
        return "The breeze is strong today, good luck walking to class"
    else:
        return "Prepare to fly"


# Humidity Recommendation
def humidity_rec(humidity):
    if humidity < 30:
        return "Bit dry out today, moisturize and hydrate"
    elif humidity < 55:
        return "Normal conditions"
    elif humidity < 65:
        return "Air is sticky"
    else:
        return "Moist. Very Moist. Unhealthy."


# Additional Recommendations
def add_rec(desc):
    if "rain" in desc:
        return "Bring an umbrella if going out"
    if "thunder" in desc:
        return "Thunder! Stay inside or keep yourself short if going outside"
    if "snow" in desc:
        return "Bring snow gear"
    if "fog" in desc:
        "Drive carefully, use low-beams"
    else:
        return "No Notes"
