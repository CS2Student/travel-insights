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
    celsius = round(kelvin - 273.15, 2)
    fahrenheit = round(celsius * (9/5) + 32, 2)
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


# jetlag_rec auxilliary
def jetlag_rec_aux(desired_sleep_time, time_difference):
    # Origin time ahead of destination time
    if time_difference > 0:
        pass
    # Destination time ahead of origin time
    else:
        pass

    sleep_time_rec = (desired_sleep_time + time_difference) % 1440
    rec_mins = int(sleep_time_rec % 60)
    rec_hrs = int((sleep_time_rec - rec_mins) / 60)

    return f"{rec_hrs:02d}:{rec_mins:02d}"


# Calculate when to sleep to avoid jetlag
def jetlag_rec(sleep_time, origin, destination):
    hours, mins = map(int, sleep_time.split(':'))
    total_mins = (hours * 60) + mins

    if ((hours < 0 or hours > 24 or mins < 0 or mins > 59) or (hours == 24 and mins != 0)):
        return False
    else:
        # Fetch City Information
        origin_data = get_forecast(origin)
        destination_data = get_forecast(destination)

        # Extract UTC time
        origin_time = origin_data['timezone']
        destination_time = destination_data['timezone']
        # Convert seconds into mins
        time_difference = (origin_time - destination_time) / 60

        # Calculate when to sleep
        sleep_time_rec = jetlag_rec_aux(total_mins, time_difference)
        return sleep_time_rec


def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: python main.py <city>                 : (City Weather Report)")
        print("Usage: python main.py <origin> <destination> : (Avoiding Jetlag Report)")
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
        # Get City Data
        city1 = sys.argv[1]
        city2 = sys.argv[2]

        # Get desired sleep time
        while True:
            try:
                print('Usage: 24 hr clock | Usage: HH:MM | Ex. 10:30')
                time_input = input(
                    "When you arrive at your destination, what time would you like to set as your desired sleep time?: ")
                rec_time = jetlag_rec(time_input, city1, city2)
                if rec_time:
                    print(f"SLEEP AT {rec_time} LOCAL TIME")
                    print("In order to prepare yourself for this sleep schedule, spend the days leading up to your trip getting closer to this sleep time.")
                    print("To ease into this sleep schedule, it is recommended you sleep one hour closer to this time each day until you get to your desired sleep time")
                    print("Having done this, you should be able to then travel to your desired destination jetlag free! Use this program again when you are ready to travel back! :)")
                    break
            except (ValueError, IndexError):
                pass


if __name__ == "__main__":
    main()
