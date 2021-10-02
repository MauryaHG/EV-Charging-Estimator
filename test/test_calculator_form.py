import unittest
from unittest import mock
from unittest.mock import Mock, patch, MagicMock

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
            field = Mock()
            form = Calculator_Form()

            # Test case: Check if None given as battery capacity, validation error is returned
            field.data = None
            try:
                form.validate_BatteryPackCapacity(field)
            except ValidationError as msg:
                self.assertEqual('Field data is none', str(msg))

            # Test case: Check if empty string  given as battery capacity, value error is returned
            field.data = ''
            try:
                form.validate_BatteryPackCapacity(field)
            except ValueError as msg:
                self.assertEqual('Cannot fetch data', str(msg))

            # Test case: Check if very large battery capacity is given, value error is returned
            field.data = '1000'
            try:
                form.validate_BatteryPackCapacity(field)
            except ValueError as msg:
                self.assertEqual('Please enter a valid battery capacity', str(msg))
                pass

    @mock.patch('app.calculator_form.Calculator_Form.FinalCharge', 100)
    def test_validate_InitialCharge(self):
        """Testing for validate_InitialCharge()"""
        with main.ev_calculator_app.app_context():
            field = Mock()
            form = Calculator_Form()

            # Test case: Check if None given as InitialCharge, validation error is returned
            field.data = None
            try:
                form.validate_InitialCharge(field)
            except ValidationError as msg:
                self.assertEqual('Field data is none', str(msg))

            # Test case: Check if empty string  given as InitialCharge, value error is returned
            field.data = ''
            try:
                form.validate_InitialCharge(field)
            except ValueError as msg:
                self.assertEqual('Cannot fetch data', str(msg))

            # Test case: Check if InitialCharge greater than 100 is given, value error is returned
            field.data = '150'
            form.FinalCharge = MagicMock()
            try:
                form.validate_InitialCharge(field)
            except ValueError as msg:
                self.assertEqual('Initial charge data error', str(msg))

    def test_validate_FinalCharge(self):
        """Testing for validate_FinalCharge()"""
        with main.ev_calculator_app.app_context():
            field = Mock()
            form = Calculator_Form()

            # Test case: Check if None given as FinalCharge, validation error is returned
            field.data = None
            try:
                form.validate_FinalCharge(field)
            except ValidationError as msg:
                self.assertEqual('Field data is none', str(msg))

            # Test case: Check if empty string  given as FinalCharge, value error is returned
            field.data = ""
            try:
                form.validate_FinalCharge(field)
            except ValueError as msg:
                self.assertEqual('Cannot fetch data', str(msg))

            # Test case: Check if FinalCharge less than 1 is given, value error is returned
            field.data = "0"
            form.InitialCharge = MagicMock()
            try:
                form.validate_FinalCharge(field)
            except ValueError as msg:
                self.assertEqual('Final charge data error', str(msg))

    def test_validate_StartDate(self):
        """Testing for validate_StartDate()"""
        with main.ev_calculator_app.app_context():
            field = Mock()
            form = Calculator_Form()

            # Test case: Check if None given as start date, validation error is returned
            field.data = None
            try:
                form.validate_StartDate(field)
            except ValidationError as msg:
                self.assertEqual('Field data is none', str(msg))

            # Test case: Check if empty string  given as start date, value error is returned
            field.data = ''
            try:
                form.validate_StartDate(field)
            except ValueError as msg:
                self.assertEqual('Cannot fetch data', str(msg))

            # Test case: Check if invalid start date is given, value error is returned
            field.data = datetime(2002, 5, 5).date()
            try:
                form.validate_StartDate(field)
            except ValueError as msg:
                self.assertEqual('Please enter a date from 01/07/2008 onwards', str(msg))

    def test_validate_StartTime(self):
        """Testing for validate_StartTime()"""
        with main.ev_calculator_app.app_context():
            field = Mock()
            form = Calculator_Form()

            # Test case: Check if None given as start time, validation error is returned
            field.data = None
            try:
                form.validate_StartTime(field)
            except ValidationError as msg:
                self.assertEqual('Field data is none', str(msg))

            # Test case: Check if empty string  given as start time, value error is returned
            field.data = ''
            try:
                form.validate_StartTime(field)
            except ValueError as msg:
                self.assertEqual('Cannot fetch data', str(msg))

    def test_validate_ChargerConfiguration(self):
        """Testing for validate_ChargerConfiguration()"""
        with main.ev_calculator_app.app_context():
            field = Mock()
            form = Calculator_Form()

            # Test case: Check if None given as ChargerConfiguration, validation error is returned
            field.data = None
            try:
                form.validate_ChargerConfiguration(field)
            except ValidationError as msg:
                self.assertEqual('Field data is none', str(msg))

            # Test case: Check if empty string  given as ChargerConfiguration, value error is returned
            field.data = ''
            try:
                form.validate_ChargerConfiguration(field)
            except ValueError as msg:
                self.assertEqual('Cannot fetch data', str(msg))

            # Test case: Check if invalid ChargerConfiguration is given, value error is returned
            field.data = '9'
            try:
                form.validate_ChargerConfiguration(field)
            except ValueError as msg:
                self.assertEqual('Please enter a valid configuration number', str(msg))

    def test_validate_PostCode(self):
        """Testing for validate_PostCode()"""
        with main.ev_calculator_app.app_context():
            field = Mock()
            form = Calculator_Form()

            # Test case: Check if None given as PostCode, validation error is returned
            field.data = None
            try:
                form.validate_PostCode(field)
            except ValidationError as msg:
                self.assertEqual('Field data is none', str(msg))

            # Test case: Check if empty string  given as PostCode, value error is returned
            field.data = ''
            try:
                form.validate_PostCode(field)
            except ValueError as msg:
                self.assertEqual('Cannot fetch data', str(msg))

            # Test case: Check if invalid PostCode is given, value error is returned
            field.data = '1000'
            try:
                form.validate_PostCode(field)
            except ValueError as msg:
                self.assertEqual('Please enter a valid Australian post code', str(msg))

if __name__ == '__main__':
    unittest.main()