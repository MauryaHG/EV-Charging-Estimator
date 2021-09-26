from app.calculator import *
import unittest


class TestCalculator(unittest.TestCase):

    def test_get_price_and_power(self):
        # Test case 1: Charger configuration 1
        calculator = Calculator("100", "50", "100", "01/02/2021", "00:00", "1", "3168")
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 5)
        self.assertEqual(calculator.power, 2)

        # Test case 2: Charger configuration 2
        calculator.charger_configuration = 2
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 7.5)
        self.assertEqual(calculator.power, 3.6)

        # Test case 3: Charger configuration 3
        calculator.charger_configuration = 3
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 10)
        self.assertEqual(calculator.power, 7.2)

        # Test case 4: Charger configuration 4
        calculator.charger_configuration = 4
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 12.5)
        self.assertEqual(calculator.power, 11)

        # Test case 5: Charger configuration 5
        calculator.charger_configuration = 5
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 15)
        self.assertEqual(calculator.power, 22)

        # Test case 6: Charger configuration 6
        calculator.charger_configuration = 6
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 20)
        self.assertEqual(calculator.power, 36)

        # Test case 7: Charger configuration 7
        calculator.charger_configuration = 7
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 30)
        self.assertEqual(calculator.power, 90)

        # Test case 8: Charger configuration 8
        calculator.charger_configuration = 8
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 50)
        self.assertEqual(calculator.power, 350)

        # Test case 9: An invalid charger configuration smaller than 1
        calculator.charger_configuration = 0
        self.assertRaises(Exception, calculator.get_price_and_power())

        # Test case 10: An invalid charger configuration greater than 8
        calculator.charger_configuration = 9
        self.assertRaises(Exception, calculator.get_price_and_power())

    def test_is_holiday(self):
        # Test case 11: ACT (Canberra Day)
        calculator = Calculator("100", "50", "100", "08/03/2021", "02:00", "1", "2601")
        self.assertTrue(calculator.is_holiday())

        # Test case 12: NSW (Bank Holiday)
        calculator = Calculator("100", "50", "100", "02/08/2021", "02:00", "1", "2666")
        self.assertTrue(calculator.is_holiday())

        # Test case 13: VIC (AFL Grand Final)
        calculator = Calculator("100", "50", "100", "24/09/2021", "02:00", "1", "3123")
        self.assertTrue(calculator.is_holiday())

        # Test case 14: QLD (Royal Queensland Show)
        calculator = Calculator("100", "50", "100", "11/08/2021", "02:00", "1", "4022")
        self.assertTrue(calculator.is_holiday())

        # Test case 15: SA (Adelaide Cup Day)
        calculator = Calculator("100", "50", "100", "08/03/2021", "02:00", "1", "5555")
        self.assertTrue(calculator.is_holiday())

        # Test case 16: WA (Anzac Day, Additional)
        calculator = Calculator("100", "1", "100", "26/04/2021", "02:00", "1", "6666")
        self.assertTrue(calculator.is_holiday())

        # Test case 17: TAS (Eight Hours Day)
        calculator = Calculator("100", "1", "100", "08/03/2021", "02:00", "1", "7777")
        self.assertTrue(calculator.is_holiday())

        # Test case 18: A non-holiday
        calculator = Calculator("100", "1", "100", "21/09/2021", "02:00", "1", "3168")
        self.assertFalse(calculator.is_holiday())

    def test_is_weekday(self):
        # Test case 19: Monday
        calculator = Calculator("66", "1", "98", "20/09/2021", "06:28", "1", "1234")
        self.assertTrue(calculator.is_weekday())

        # Test case 20: Tuesday
        calculator = Calculator("66", "1", "98", "21/09/2021", "06:28", "1", "1234")
        self.assertTrue(calculator.is_weekday())

        # Test case 21: Wednesday
        calculator = Calculator("66", "1", "98", "22/09/2021", "06:28", "1", "1234")
        self.assertTrue(calculator.is_weekday())

        # Test case 22: Thursday
        calculator = Calculator("66", "1", "98", "23/09/2021", "06:28", "1", "1234")
        self.assertTrue(calculator.is_weekday())

        # Test case 23: Friday
        calculator = Calculator("66", "1", "98", "24/09/2021", "06:28", "1", "1234")
        self.assertTrue(calculator.is_weekday())

        # Test case 24: Saturday
        calculator = Calculator("66", "1", "98", "25/09/2021", "06:28", "1", "1234")
        self.assertFalse(calculator.is_weekday())

        # Test case 25: Sunday
        calculator = Calculator("66", "1", "98", "26/09/2021", "06:28", "1", "1234")
        self.assertFalse(calculator.is_weekday())

    def test_time_calculation(self):
        pass

    def test_cost_calculation(self):
        # Just a random example from spec, to be rewritten
        calculator = Calculator("82", "20", "80", "21/09/2021", "14:30", "8", "3168")
        self.assertAlmostEqual(float(calculator.cost_calculation()), 27.06)

    # you may create test suite if needed
    if __name__ == "__main__":
        pass
