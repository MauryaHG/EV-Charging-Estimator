from app.calculator import *
import unittest


class TestCalculator(unittest.TestCase):
    """Unit tests for Calculator class"""

    def test_get_price_and_power(self):
        """Testing for get_price_and_power()"""

        # Test case 1: Charger configuration 1
        calculator = Calculator("100", "50", "100", "01/02/2021", "00:00", "1", "3168")
        calculator.get_price_and_power()
        self.assertEqual(5, calculator.base_price)
        self.assertEqual(2, calculator.power)

        # Test case 2: Charger configuration 2
        calculator.charger_configuration = 2
        calculator.get_price_and_power()
        self.assertEqual(7.5, calculator.base_price)
        self.assertEqual(3.6, calculator.power, )

        # Test case 3: Charger configuration 3
        calculator.charger_configuration = 3
        calculator.get_price_and_power()
        self.assertEqual(10, calculator.base_price)
        self.assertEqual(7.2, calculator.power)

        # Test case 4: Charger configuration 4
        calculator.charger_configuration = 4
        calculator.get_price_and_power()
        self.assertEqual(12.5, calculator.base_price)
        self.assertEqual(11, calculator.power, )

        # Test case 5: Charger configuration 5
        calculator.charger_configuration = 5
        calculator.get_price_and_power()
        self.assertEqual(15, calculator.base_price)
        self.assertEqual(22, calculator.power)

        # Test case 6: Charger configuration 6
        calculator.charger_configuration = 6
        calculator.get_price_and_power()
        self.assertEqual(20, calculator.base_price)
        self.assertEqual(36, calculator.power)

        # Test case 7: Charger configuration 7
        calculator.charger_configuration = 7
        calculator.get_price_and_power()
        self.assertEqual(30, calculator.base_price)
        self.assertEqual(90, calculator.power)

        # Test case 8: Charger configuration 8
        calculator.charger_configuration = 8
        calculator.get_price_and_power()
        self.assertEqual(50, calculator.base_price)
        self.assertEqual(350, calculator.power)

    def test_is_holiday(self):
        """Testing for is_holiday()"""

        # Test case 9: NT (May Day)
        calculator = Calculator("100", "50", "100", "03/05/2021", "02:00", "1", "888")
        self.assertTrue(calculator.is_holiday())

        # Test case 10: ACT (Canberra Day)
        calculator = Calculator("100", "50", "100", "08/03/2021", "02:00", "1", "2601")
        self.assertTrue(calculator.is_holiday())

        # Test case 11: NSW (Bank Holiday)
        calculator = Calculator("100", "50", "100", "02/08/2021", "02:00", "1", "2666")
        self.assertTrue(calculator.is_holiday())

        # Test case 12: VIC (AFL Grand Final)
        calculator = Calculator("100", "50", "100", "24/09/2021", "02:00", "1", "3123")
        self.assertTrue(calculator.is_holiday())

        # Test case 13: QLD (The day after Good Friday)
        calculator = Calculator("100", "50", "100", "03/04/2021", "02:00", "1", "4022")
        self.assertTrue(calculator.is_holiday())

        # Test case 14: SA (Adelaide Cup Day)
        calculator = Calculator("100", "50", "100", "08/03/2021", "02:00", "1", "5555")
        self.assertTrue(calculator.is_holiday())

        # Test case 15: WA (Anzac Day, Additional)
        calculator = Calculator("100", "1", "100", "26/04/2021", "02:00", "1", "6666")
        self.assertTrue(calculator.is_holiday())

        # Test case 16: TAS (Eight Hours Day)
        calculator = Calculator("100", "1", "100", "08/03/2021", "02:00", "1", "7777")
        self.assertTrue(calculator.is_holiday())

        # Test case 17: Non-holidays
        calculator = Calculator("100", "1", "100", "21/09/2021", "02:00", "1", "3168")
        self.assertFalse(calculator.is_holiday())

        # Test case 18: Non-holidays
        calculator = Calculator("100", "1", "100", "01/08/2021", "02:00", "1", "4321")
        self.assertFalse(calculator.is_holiday())

        # Test case 19: Non-holidays
        calculator = Calculator("100", "1", "100", "30/12/2009", "02:00", "1", "5678")
        self.assertFalse(calculator.is_holiday())

    def test_is_weekday(self):
        """Testing for is_weekday()"""

        # Test case 20: Monday
        calculator = Calculator("66", "1", "98", "20/09/2021", "06:28", "1", "1234")
        self.assertTrue(calculator.is_weekday())

        # Test case 21: Tuesday
        calculator = Calculator("66", "1", "98", "21/09/2021", "06:28", "1", "1234")
        self.assertTrue(calculator.is_weekday())

        # Test case 22: Wednesday
        calculator = Calculator("66", "1", "98", "22/09/2021", "06:28", "1", "1234")
        self.assertTrue(calculator.is_weekday())

        # Test case 23: Thursday
        calculator = Calculator("66", "1", "98", "23/09/2021", "06:28", "1", "1234")
        self.assertTrue(calculator.is_weekday())

        # Test case 24: Friday
        calculator = Calculator("66", "1", "98", "24/09/2021", "06:28", "1", "1234")
        self.assertTrue(calculator.is_weekday())

        # Test case 25: Saturday
        calculator = Calculator("66", "1", "98", "25/09/2021", "06:28", "1", "1234")
        self.assertFalse(calculator.is_weekday())

        # Test case 26: Sunday
        calculator = Calculator("66", "1", "98", "26/09/2021", "06:28", "1", "1234")
        self.assertFalse(calculator.is_weekday())

    def test_time_calculation(self):
        """Testing for time_calculation()"""

        # Test case 27: An usual charging time that is less than 1 hour
        calculator = Calculator("82", "20", "80", "21/09/2021", "14:30", "8", "3168")
        self.assertAlmostEqual(8.43, calculator.time_calculation(), 2)

        # Test case 28: An usual charging time that is more than 1 hour
        calculator = Calculator("82", "20", "80", "21/09/2021", "14:30", "5", "3168")
        self.assertAlmostEqual(134.18, calculator.time_calculation(), 2)

        # Test case 29: An unusually small charging time
        calculator = Calculator("82", "0", "1", "21/09/2021", "14:30", "8", "3168")
        self.assertAlmostEqual(0.14, calculator.time_calculation(), 2)

        # Test case 30: An unusually large charging time
        calculator = Calculator("82", "0", "100", "21/09/2021", "14:30", "1", "3168")
        self.assertEqual(2460, calculator.time_calculation())

    def test_cost_calculation(self):
        """Testing for cost_calculation()"""

        # Test case 31: Normal weekday charging during peak hours
        calculator = Calculator("82", "20", "80", "21/09/2021", "14:30", "8", "3168")
        self.assertEqual(27.1, calculator.cost_calculation())

        # Test case 32: Normal weekend charging during peak hours
        calculator = Calculator("82", "20", "80", "25/09/2021", "14:30", "8", "3168")
        self.assertEqual(24.6, calculator.cost_calculation())

        # Test case 33: Normal weekday charging during off-peak hours
        calculator = Calculator("82", "20", "80", "21/09/2021", "22:30", "8", "3168")
        self.assertEqual(13.5, calculator.cost_calculation())

        # Test case 34: Normal weekend charging during off-peak hours
        calculator = Calculator("82", "20", "80", "25/09/2021", "22:30", "8", "3168")
        self.assertEqual(12.3, calculator.cost_calculation())

        # Test case 35: Holiday charging during peak hours
        calculator = Calculator("82", "20", "80", "24/09/2021", "14:30", "8", "3168")
        self.assertEqual(27.1, calculator.cost_calculation())

        # Test case 36: Holiday charging during off-peak hours
        calculator = Calculator("82", "20", "80", "24/09/2021", "22:30", "8", "3168")
        self.assertEqual(13.5, calculator.cost_calculation())

        # Test case 37: Charging across peak & off-peak hours
        calculator = Calculator("82", "20", "80", "24/09/2021", "17:00", "5", "3168")
        self.assertEqual(5.9, calculator.cost_calculation())

        # Test case 38: Charging across off-peak & peak hours
        calculator = Calculator("82", "20", "80", "24/09/2021", "05:00", "5", "3168")
        self.assertEqual(6.3, calculator.cost_calculation())

        # Test case 39: Charging spanning across multiple peak & off-peak periods and weekday & weekend
        calculator = Calculator("82", "0", "100", "19/09/2021", "14:00", "1", "3168")
        self.assertEqual(3.1, calculator.cost_calculation())

    def test_get_weather_data(self):
        """Testing for get_weather_data()"""

        # Test case 40: Test if method returns accurate data
        requestURL = "http://118.138.246.158/api/v1/weather?location=80593519-8dd0-4d1e-9307-43e280a4e3f4&date=2020-09-18"
        response = requests.get(requestURL)

        calculator = Calculator("100", "0", "100", "18/09/2020", "12:00", "1", "3000")
        self.assertEqual(response.json(), calculator.get_weather_data())

        # Test case 41: Test if method returns accurate data when  specific date given
        self.assertEqual("2021-05-15", calculator.get_weather_data('2021-05-15')["date"])

    def test_get_state_id(self):
        """Testing for get_state_id()"""

        # Test case 42: Test if method returns accurate data
        requestURL = "http://118.138.246.158/api/v1/location?postcode=3800"
        response = requests.get(requestURL)

        calculator = Calculator("100", "0", "100", "18/09/2020", "12:00", "1", "3800")
        self.assertEqual(response.json()[0]["id"], calculator.get_state_id())
