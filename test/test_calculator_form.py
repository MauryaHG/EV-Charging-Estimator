import unittest
import main

from app.calculator_form import *


class TestCalculatorForm(unittest.TestCase):
    """Unit tests for Calculator_Form class"""

    def setUp(self):
        """Configure the test class"""
        main.ev_calculator_app.config['TESTING'] = True
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False

    def test_validate_BatteryPackCapacity(self):
        """Testing for validate_BatteryPackCapacity()"""
        with main.ev_calculator_app.app_context():
            form = Calculator_Form()
            # Test case:
            pass

    def test_validate_InitialCharge(self):
        """Testing for validate_InitialCharge()"""
        pass

    def test_validate_FinalCharge(self):
        """Testing for validate_FinalCharge()"""
        pass

    def test_validate_StartDate(self):
        """Testing for validate_StartDate()"""
        pass

    def test_validate_StartTime(self):
        """Testing for validate_StartTime()"""
        pass

    def test_validate_ChargerConfiguration(self):
        """Testing for validate_ChargerConfiguration()"""
        pass

    def test_validate_PostCode(self):
        """Testing for validate_PostCode()"""
        pass
