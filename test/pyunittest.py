from app.calculator import *
import unittest


class TestCalculator(unittest.TestCase):

    def test_get_price_and_power(self):
        # Test case for charger configuration 1
        calculator = Calculator("100", "50", "100", "01/02/2021", "00:00", "1", "3168")
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 5)
        self.assertEqual(calculator.power, 2)

        # Test case for charger configuration 2
        calculator.charger_configuration = 2
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 7.5)
        self.assertEqual(calculator.power, 3.6)

        # Test case for charger configuration 3
        calculator.charger_configuration = 3
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 10)
        self.assertEqual(calculator.power, 7.2)

        # Test case for charger configuration 4
        calculator.charger_configuration = 4
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 12.5)
        self.assertEqual(calculator.power, 11)

        # Test case for charger configuration 5
        calculator.charger_configuration = 5
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 15)
        self.assertEqual(calculator.power, 22)

        # Test case for charger configuration 6
        calculator.charger_configuration = 6
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 20)
        self.assertEqual(calculator.power, 36)

        # Test case for charger configuration 7
        calculator.charger_configuration = 7
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 30)
        self.assertEqual(calculator.power, 90)

        # Test case for charger configuration 8
        calculator.charger_configuration = 8
        calculator.get_price_and_power()
        self.assertEqual(calculator.base_price, 50)
        self.assertEqual(calculator.power, 350)

        # Test case for invalid charger configurations
        calculator.charger_configuration = 0
        self.assertRaises(Exception, calculator.get_price_and_power())
        calculator.charger_configuration = 9
        self.assertRaises(Exception, calculator.get_price_and_power())

    def test_cost(self):
        # Example from spec
        calculator = Calculator("82", "20", "80", "21/09/2021", "14:30", "8", "3168")
        self.assertAlmostEqual(float(calculator.cost_calculation()), 27.06)

    # you may create test suite if needed
    if __name__ == "__main__":
        pass
