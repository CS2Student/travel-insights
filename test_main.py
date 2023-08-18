import unittest
import main


class TestCalc(unittest.TestCase):

    def test_kelvin_to_celsius_fahrenheit(self):
        celsius, fahrenheit = main.kelvin_to_celsius_fahrenheit(0)
        self.assertEqual(celsius, -273.15)
        self.assertEqual(fahrenheit, -459.67)

    # Test Origin time ahead of Destination time
    def test_jetlag_rec_OAD(self):
        result = main.jetlag_rec("10:00", "New York", "Hawaii")
        self.assertEqual(result, "16:00")

    # Test Destination time ahead of Origin time
    def test_jetlag_rec_DAO(self):
        result = main.jetlag_rec("22:30", "New York", "Beijing")
        self.assertEqual(result, "10:30")

    # Test Origin Time same as Destination Time
    def test_jetlag_rec_equal(self):
        result = main.jetlag_rec("00:30", "New York", "Toronto")
        self.assertEqual(result, "00:30")

     # Test time = 00:00
    def test_jetlag_rec_0(self):
        result = main.jetlag_rec("00:00", "New York", "Toronto")
        self.assertEqual(result, "00:00")

    # Test time = 24:00, works because 24:00 == 00:00 in 24 hr time
    def test_jetlag_rec_24(self):
        result = main.jetlag_rec("24:00", "New York", "Toronto")
        self.assertEqual(result, "00:00")

    # Tests time > 24
    def test_jetlag_rec_over(self):
        result = main.jetlag_rec("24:01", "New York", "Toronto")
        self.assertEqual(result, False)


if __name__ == '__main__':
    unittest.main()
