import math

from flask import Flask, flash
from flask import render_template
from flask import request
from app.calculator import *

from app.calculator_form import *
import os

SECRET_KEY = os.urandom(32)

ev_calculator_app = Flask(__name__)
ev_calculator_app.config['SECRET_KEY'] = SECRET_KEY


@ev_calculator_app.route('/', methods=['GET', 'POST'])
def operation_result():
    """Output the calculation result"""
    # request.form looks for:
    # html tags with matching "name="

    calculator_form = Calculator_Form(request.form)

    # validation of the form
    if request.method == "POST" and calculator_form.validate():
        # extract information from the form
        battery_capacity = request.form['BatteryPackCapacity']
        initial_charge = request.form['InitialCharge']
        final_charge = request.form['FinalCharge']
        start_date = request.form['StartDate']
        start_time = request.form['StartTime']
        charger_configuration = request.form['ChargerConfiguration']
        post_code = request.form['PostCode']

        # if valid, create calculator to calculate the time and cost
        calculator = Calculator(battery_capacity, initial_charge, final_charge, start_date, start_time, charger_configuration, post_code)

        charging_time = calculator.time_calculation()
        charging_cost = calculator.cost_calculation()
        charging_cost_2 = calculator.req2()
        charging_cost_3 = calculator.calculate_cost_alg3()


        hours = math.floor(charging_time / 60)
        minutes = charging_time % 60
        output_time = '{} hours {:.0f} minutes'.format(hours, minutes)
        output_cost = "Cost of normal charging $ " + str(charging_cost)
        output_cost_2 = "Cost with solar energy:$ {:.2f}".format(charging_cost_2)
        output_cost_3 = "Cost with solar energy and cloud cover$ {:.2f}".format(charging_cost_3)


        # you may change the return statement also

        # values of variables can be sent to the template for rendering the webpage that users will see return
        # render_template('calculator.html', cost = cost, time = time, calculation_success = True,
        # form = calculator_form)
        return render_template('calculator.html', time=output_time, cost=output_cost, cost_2=output_cost_2, cost_3=output_cost_3, calculation_success=True,
                               form=calculator_form)
    else:
        # battery_capacity = request.form['BatteryPackCapacity']
        # flash(battery_capacity)
        # flash("something went wrong")
        flash_errors(calculator_form)
        return render_template('calculator.html', calculation_success=False, form=calculator_form)


# method to display all errors
def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


if __name__ == '__main__':
    ev_calculator_app.run()
