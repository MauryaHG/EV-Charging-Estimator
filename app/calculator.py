import holidays
from datetime import datetime
from time import time


class Calculator():
    # you can choose to initialise variables here, if needed.
    def __init__(self, battery_capacity, initial_charge, final_charge, start_date, start_time, charger_configuration, post_code):
        self.battery_capacity = battery_capacity
        self.initial_charge = initial_charge
        self.final_charge = final_charge
        self.start_date = start_date
        self.start_time = start_time
        self.charger_configuration = int(charger_configuration)
        self.post_code = int(post_code)

    # you may add more parameters if needed, you may modify the formula also.
    def cost_calculation(self, initial_state, final_state, capacity, is_peak, is_holiday):
        if is_peak:
            base_price = 100
        else:
            base_price = 50

        if is_holiday:
            surcharge_factor = 1.1
        else:
            surcharge_factor = 1

        charging_cost = (final_state - initial_state) / 100 * capacity * base_price / 100 * surcharge_factor
        return charging_cost

    # you may add more parameters if needed, you may also modify the formula.
    def time_calculation(self, initial_state, final_state, capacity):
        if self.charger_configuration == 1:
            power = 2
        elif self.charger_configuration == 2:
            power = 3.6
        elif self.charger_configuration == 3:
            power = 7.2
        elif self.charger_configuration == 4:
            power = 11
        elif self.charger_configuration == 5:
            power = 22
        elif self.charger_configuration == 6:
            power = 36
        elif self.charger_configuration == 7:
            power = 90
        elif self.charger_configuration == 8:
            power = 350
        else:
            raise Exception("Invalid configuration number")
        charging_time = (final_state - initial_state) / 100 * capacity / power
        return charging_time

    # you may create some new methods at your convenience, or modify these methods, or choose not to use them.
    def is_holiday(self):
        # Get state from post code
        if 800 <= self.post_code < 1000:
            prov = 'NT'
        elif 1000 <= self.post_code < 2600 or 2619 <= self.post_code < 2900 or 2921 <= self.post_code < 3000:
            prov = 'NSW'
        elif 3000 <= self.post_code < 4000 or 8000 <= self.post_code < 9000:
            prov = 'VIC'
        elif 4000 <= self.post_code < 5000 or 9000 <= self.post_code < 10000:
            prov = 'QLD'
        elif 5000 <= self.post_code < 6000:
            prov = 'SA'
        elif 6000 <= self.post_code < 7000:
            prov = 'WA'
        elif 7000 <= self.post_code < 8000:
            prov = 'TAS'
        else:
            raise Exception("Invalid post code")
        aus_state_holidays = holidays.CountryHoliday('AUS', prov)
        return self.start_date in aus_state_holidays

    def is_peak(self):
        time.strptime(self.start_time, '%X')
        return '06:00' <= self.start_time <= '18:00'

    def peak_period(self, start_time):
        pass

    def get_duration(self, start_time):
        pass

    # to be acquired through API
    def get_sun_hour(self, sun_hour):
        pass

    # to be acquired through API
    def get_solar_energy_duration(self, start_time):
        pass

    # to be acquired through API
    def get_day_light_length(self, start_time):
        pass

    # to be acquired through API
    def get_solar_insolation(self, solar_insolation):
        pass

    # to be acquired through API
    def get_cloud_cover(self):
        pass

    def calculate_solar_energy(self):
        pass
