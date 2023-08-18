import unittest
from unittest.mock import Mock, patch
import datetime as dt
import main  # Import your program's module


class TestMain(unittest.TestCase):

    @patch('main.requests.get')
    def test_get_forecast(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'temperature': 25, 'humidity': 60}
        mock_get.return_value = mock_response

        forecast_data = main.get_forecast('New York')
        self.assertEqual(forecast_data, {'temperature': 25, 'humidity': 60})

    def test_kelvin_to_celsius_fahrenheit(self):
        celsius, fahrenheit = main.kelvin_to_celsius_fahrenheit(300)
        self.assertAlmostEqual(celsius, 26.85, places=2)
        self.assertAlmostEqual(fahrenheit, 80.33, places=2)

    def test_temp_rec(self):
        self.assertEqual(main.temp_rec(5), "JACKET, SWEATPANTS, WINTER SHOES")
        self.assertEqual(main.temp_rec(
            15), "SWEATER, SWEATPANTS, CASUAL SHOES")
        self.assertEqual(main.temp_rec(30), "SHORTS, RUNNING SHOES")
        self.assertEqual(main.temp_rec(38), "HEAT WAVE")

    def test_wind_rec(self):
        self.assertEqual(main.wind_rec(3), "It's calm outside")
        self.assertEqual(main.wind_rec(
            8), "There is a moderate breeze outside")
        self.assertEqual(main.wind_rec(
            15), "The breeze is strong today, good luck walking outside")
        self.assertEqual(main.wind_rec(25), "Prepare to fly")

    def test_humidity_rec(self):
        self.assertEqual(main.humidity_rec(
            20), "Bit dry out today, moisturize and hydrate")
        self.assertEqual(main.humidity_rec(45), "Normal conditions")
        self.assertEqual(main.humidity_rec(60), "Air is sticky")
        self.assertEqual(main.humidity_rec(
            75), "Moist. Very Moist. Unhealthy.")

    def test_add_rec(self):
        self.assertEqual(main.add_rec("light rain"),
                         "Bring an umbrella if going out")
        self.assertEqual(main.add_rec(
            "thunderstorm"), "Thunder! Stay inside or keep yourself short if going outside")
        self.assertEqual(main.add_rec("snowing"), "Bring snow gear")
        self.assertEqual(main.add_rec("foggy"), "No Notes")

    def test_jetlag_rec_aux(self):
        rec_time = main.jetlag_rec_aux(600, 180)  # 10:00 + 3 hrs = 13:00
        self.assertEqual(rec_time, "13:00")

    @patch('main.get_forecast')
    @patch('main.dt')
    def test_jetlag_rec(self, mock_datetime, mock_get_forecast):
        mock_datetime.datetime.utcfromtimestamp.side_effect = [
            dt.datetime(2023, 8, 17, 12, 0),
            dt.datetime(2023, 8, 17, 0, 0)
        ]
        mock_get_forecast.side_effect = [
            {'timezone': -18000}, {'timezone': -36000}]

        with unittest.mock.patch('builtins.input', side_effect=["10:00"]):
            output = main.jetlag_rec("10:00", "New York", "Hawaii")

        expected_output = "SLEEP AT 13:00 LOCAL TIME"
        self.assertIn(expected_output, output)


if __name__ == '__main__':
    unittest.main()
