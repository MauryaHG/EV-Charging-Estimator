from app.calculator import *
import unittest


class TestCalculator(unittest.TestCase):

    # you may create more test methods
    # you may add parameters to test methods
    # this is an example
    def test_cost(self):
        # Example from spec
        self.calculator = Calculator("82", "20", "80", "21/09/2021", "14:30", "8", "3168")
        self.assertAlmostEqual(float(self.calculator.cost_calculation()), 27.06)

    # you may create test suite if needed
    if __name__ == "__main__":
        test_cost()
