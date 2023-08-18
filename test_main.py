import unittest
import main


class TestCalc(unittest.TestCase):

    def test_kelvin_to_celsius_fahrenheit(self):
        celsius, fahrenheit = main.kelvin_to_celsius_fahrenheit(0)
        self.assertEqual(celsius, -273.15)
        self.assertEqual(fahrenheit, -459.67)

    # Test Origin time ahead of Destination time
    def test_jetlag_rec_OAD(self):
        result = main.jetlag_rec("22:30", "New York", "Hawaii")
        self.assertEqual(result, "04:30")

    # Test Destination time ahead of Origin time
    def test_jetlag_rec_DAO(self):
        result = main.jetlag_rec("22:30", "New York", "Beijing")
        self.assertEqual(result, "10:30")


if __name__ == '__main__':
    unittest.main()
