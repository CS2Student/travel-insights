import datetime as dt
import requests
import sys

# Get API response
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
with open('api_key', 'r') as file:
    API_KEY = file.read()


def get_forecast(city):
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url).json()
    return response


# Temperature conversion function
def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit


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
        return "The breeze is strong today, good luck walking outside"
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


# Calculate when to sleep to avoid jetlag
def jetlag_rec(sleep_time):
    hours, mins = map(int, sleep_time.split(':'))
    total_mins = (hours * 60) + mins

    if (total_mins < 0 or total_mins > 1440):
        print('Invalid Time')
        return False
    else:
        # Calculate when to sleep
        # Print when to sleep
        return True


def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: python main.py <city>                : (City Weather Report)")
        print("Usage: python main.py <city> <another city> : (Avoiding Jetlag Report)")
        sys.exit(1)

    # City Weather Report
    if len(sys.argv) == 2:
        city = sys.argv[1]

        forecast_data = get_forecast(city)
        print(forecast_data)

        # Parse necessary values
        temp_kelvin = forecast_data['main']['temp']
        temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(
            temp_kelvin)
        feels_like_kelvin = forecast_data['main']['feels_like']
        feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(
            feels_like_kelvin)
        wind_speed = forecast_data['wind']['speed']
        humidity = forecast_data['main']['humidity']
        description = forecast_data['weather'][0]['description']
        sunrise_time = dt.datetime.utcfromtimestamp(
            forecast_data['sys']['sunrise'] + forecast_data['timezone'])
        sunset_time = dt.datetime.utcfromtimestamp(
            forecast_data['sys']['sunset'] + forecast_data['timezone'])

        # Message
        print(f'------------------------{city.upper()}----------------------')
        print(f'Temperature: {temp_celsius:.2f}°C | {temp_fahrenheit:.2f}°F')
        print(
            f'Feels like : {feels_like_celsius:.2f}°C | {feels_like_fahrenheit:.2f}°F')
        print(f'Wind Speed: {wind_speed}m/s')
        print(f'Humidity: {humidity}%')
        print(f'Sunrise: {sunrise_time}')
        print(f'Sunset: {sunset_time}')
        print(f"Description: {description}")

        # Report
        print(f'------------------------REPORT----------------------------')
        print('CLOTHES: ' + temp_rec(temp_celsius))
        print('WIND: ' + wind_rec(wind_speed))
        print('HUMIDITY: ' + humidity_rec(humidity))
        print('OTHER: ' + add_rec(description))
        print(f'----------------------------------------------------------')

    # Avoiding Jetlag Report
    if len(sys.argv) == 3:
        # Get desired sleep time
        while True:
            try:
                print('Usage: 24 hr clock | Usage: HH:MM | Ex. 10:30')
                time_input = input(
                    "At your destination, what is your desired sleep time?: ")
                if jetlag_rec(time_input):
                    break
            except (ValueError, IndexError):
                print('Invalid Time')


if __name__ == "__main__":
    main()
