import holidays
from datetime import datetime, timedelta


def is_peak(start_datetime):
    return datetime.strptime('06:00', '%H:%M') <= start_datetime <= datetime.strptime('18:00', '%H:%M')


class Calculator:
    # you can choose to initialise variables here, if needed.
    def __init__(self, battery_capacity, initial_charge, final_charge, start_date, start_time, charger_configuration, post_code):
        self.battery_capacity = int(battery_capacity)
        self.initial_charge = int(initial_charge)
        self.final_charge = int(final_charge)
        self.start_time = datetime.strptime(start_time, '%H:%M')
        self.start_datetime = datetime.strptime(start_date + ' ' + start_time, '%d/%m/%Y %H:%M')
        self.post_code = int(post_code)
        self.charger_configuration = int(charger_configuration)
        self.base_price = 0
        self.power = 0

    def get_price_and_power(self):
        if self.charger_configuration == 1:
            self.base_price = 5
            self.power = 2
        elif self.charger_configuration == 2:
            self.base_price = 7.5
            self.power = 3.6
        elif self.charger_configuration == 3:
            self.base_price = 10
            self.power = 7.2
        elif self.charger_configuration == 4:
            self.base_price = 12.5
            self.power = 11
        elif self.charger_configuration == 5:
            self.base_price = 15
            self.power = 22
        elif self.charger_configuration == 6:
            self.base_price = 20
            self.power = 36
        elif self.charger_configuration == 7:
            self.base_price = 30
            self.power = 90
        elif self.charger_configuration == 8:
            self.base_price = 50
            self.power = 350

    # you may add more parameters if needed, you may also modify the formula.
    def time_calculation(self):
        self.get_price_and_power()
        charging_time = (self.final_charge - self.initial_charge) / 100 * self.battery_capacity / self.power
        return charging_time

    # you may add more parameters if needed, you may modify the formula also.
    def cost_calculation(self):
        charging_time = self.time_calculation()
        time_left = charging_time
        charging_cost = 0
        while time_left > 0:
            if self.is_holiday() or self.is_weekday():
                surcharge_factor = 1.1
            else:
                surcharge_factor = 1
            if is_peak(self.start_time):
                discount_factor = 1
            else:
                discount_factor = 0.5

            if time_left <= 1:
                time_factor = time_left
            else:
                time_factor = 1
                self.start_datetime += timedelta(hours=1)
            charging_cost += (self.final_charge - self.initial_charge) / 100 * self.battery_capacity * self.base_price / 100 * surcharge_factor * discount_factor * time_factor
            time_left -= 1
        charging_cost /= charging_time
        return charging_cost

    # you may create some new methods at your convenience, or modify these methods, or choose not to use them.
    def is_holiday(self):
        # Get state from post code
        if 800 <= self.post_code < 1000:
            province = 'NT'
        elif 1000 <= self.post_code < 2600 or 2619 <= self.post_code < 2900 or 2921 <= self.post_code < 3000:
            province = 'NSW'
        elif 3000 <= self.post_code < 4000 or 8000 <= self.post_code < 9000:
            province = 'VIC'
        elif 4000 <= self.post_code < 5000 or 9000 <= self.post_code < 10000:
            province = 'QLD'
        elif 5000 <= self.post_code < 6000:
            province = 'SA'
        elif 6000 <= self.post_code < 7000:
            province = 'WA'
        elif 7000 <= self.post_code < 8000:
            province = 'TAS'
        else:
            raise Exception("Invalid post code")
        aus_state_holidays = holidays.CountryHoliday('AUS', prov=province, state=None)
        return self.start_datetime in aus_state_holidays

    def is_weekday(self):
        return self.start_datetime.weekday() <= 4

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
