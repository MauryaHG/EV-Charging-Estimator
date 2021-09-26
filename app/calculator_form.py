from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField
from wtforms.validators import DataRequired, ValidationError, Optional
from datetime import datetime


# validation for form inputs
class Calculator_Form(FlaskForm):
    # this variable name needs to match with the input attribute name in the html file
    # you are NOT ALLOWED to change the field type, however, you can add more built-in validators and custom messages
    BatteryPackCapacity = StringField("Battery Pack Capacity", [DataRequired()])
    InitialCharge = StringField("Initial Charge", [DataRequired()])
    FinalCharge = StringField("Final Charge", [DataRequired()])
    StartDate = DateField("Start Date", [DataRequired("Data is missing or format is incorrect")], format='%d/%m/%Y')
    StartTime = TimeField("Start Time", [DataRequired("Data is missing or format is incorrect")], format='%H:%M')
    ChargerConfiguration = StringField("Charger Configuration", [DataRequired()])
    PostCode = StringField("Post Code", [DataRequired()])

    # use validate_ + field_name to activate the flask-wtforms built-in validator
    # this is an example for you
    def validate_BatteryPackCapacity(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValueError("Cannot fetch data")
        elif int(field.data) < 5 or int(field.data) > 150:
            raise ValueError("Please enter a valid battery capacity")

    # validate initial charge here
    def validate_InitialCharge(self, field):
        # another example of how to compare initial charge with final charge
        # you may modify this part of the code
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValueError("Cannot fetch data")
        elif int(field.data) > int(self.FinalCharge.data) or int(field.data) < 0 or int(field.data) > 99:
            raise ValueError("Initial charge data error")

    # validate final charge here
    def validate_FinalCharge(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValueError("Cannot fetch data")
        elif int(field.data) < int(self.InitialCharge.data) or int(field.data) > 100 or int(field.data) < 1:
            raise ValueError("Final charge data error")

    # validate start date here
    def validate_StartDate(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValueError("Cannot fetch data")
        elif field.data < datetime.strptime('01/07/2008', '%d/%m/%Y').date():
            raise ValueError('Please enter a date from 01/07/2008 onwards')

    # validate start time here
    def validate_StartTime(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValueError("Cannot fetch data")

    # validate charger configuration here
    def validate_ChargerConfiguration(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValueError("Cannot fetch data")
        elif int(field.data) < 1 or int(field.data) > 8:
            raise ValueError('Please enter a configuration number')

    # validate postcode here
    def validate_PostCode(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValueError("Cannot fetch data")
        elif int(field.data) > 9999 or int(field.data) < 800:
            raise ValueError("Please enter a valid Australian post code")
