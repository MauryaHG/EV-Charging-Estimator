import holidays
import requests
from datetime import datetime, timedelta


class Calculator:
    """The calculator class"""

    def __init__(self, battery_capacity, initial_charge, final_charge, start_date, start_time, charger_configuration,
                 post_code):
        """Initialisation of variables"""
        self.battery_capacity = int(battery_capacity)
        self.initial_charge = int(initial_charge)
        self.final_charge = int(final_charge)
        self.start_datetime = datetime.strptime(start_date + ' ' + start_time, '%d/%m/%Y %H:%M')
        self.post_code = int(post_code)
        self.charger_configuration = int(charger_configuration)
        self.base_price = 0
        self.power = 0

    def get_price_and_power(self):
        """Get price and power from charger configuration"""
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

    def time_calculation(self):
        """Calculation of charging time"""
        self.get_price_and_power()
        charging_time = (self.final_charge - self.initial_charge) / 100 * self.battery_capacity / self.power * 60
        return charging_time

    def cost_calculation(self):
        """Calculation of charging cost"""
        charging_time = self.time_calculation()
        time_left = charging_time
        charging_cost = 0
        # Calculation is done in per-minute basis
        while time_left > 0:
            if self.is_holiday() or self.is_weekday():
                surcharge_factor = 1.1
            else:
                surcharge_factor = 1
            if self.is_peak():
                discount_factor = 1
            else:
                discount_factor = 0.5
            if time_left >= 1:
                time_factor = 1 / charging_time
                self.start_datetime += timedelta(minutes=1)
            else:
                time_factor = time_left / charging_time
                self.start_datetime += timedelta(seconds=60 * time_left)
            charging_cost += (self.final_charge - self.initial_charge) / 100 * self.battery_capacity * self.base_price / 100 * surcharge_factor * discount_factor * time_factor
            time_left -= 1
        return round(charging_cost, 1)

    def is_holiday(self):
        """Check if the charging start date is a holiday in the state represented by postcode"""
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
            province = 'ACT'
        aus_state_holidays = holidays.CountryHoliday('AUS', prov=province, state=None)
        return self.start_datetime in aus_state_holidays

    def is_weekday(self):
        """Check if the charging start date is a weekday"""
        return self.start_datetime.weekday() <= 4

    def is_peak(self):
        """Check if the charging start time is during peak hours"""
        lower_bound = datetime.strptime(str(self.start_datetime.date()) + ' 06:00', '%Y-%m-%d %H:%M')
        upper_bound = datetime.strptime(str(self.start_datetime.date()) + ' 18:00', '%Y-%m-%d %H:%M')
        return lower_bound <= self.start_datetime <= upper_bound


    def get_sun_hour(self):
        """ Get sunhours(solar isolation for a specific date in a state)"""
        stateJson = self.get_weather_data()
        return stateJson["sunHours"]


    def get_solar_energy_duration(self):
        """ returns total hours of solar generation in hours"""
        start_time = self.start_datetime
        weather_data = self.get_weather_data()
        FMT = '%H:%M:%S'
        sunrise_time = datetime.strptime(weather_data["sunrise"], FMT)
        sunset_time = datetime.strptime(weather_data["sunset"], FMT)
        charging_time = timedelta(minutes=self.time_calculation())
        final_time = self.start_datetime + charging_time

        if start_time.time() < sunrise_time.time() and final_time <= sunset_time:
            du = (final_time - sunrise_time)
        elif start_time.time() >= sunrise_time.time() and final_time <= sunset_time:
            du = charging_time
        elif start_time.time() >= sunrise_time.time() and final_time > sunset_time:
            du = sunset_time - start_time
        elif start_time.time() < sunrise_time.time() and final_time > sunset_time:
            du = self.get_day_light_length()
        return du.seconds/3600



    """ 
     Returns  day light hours for a specific date in a state
     Output:
         float of hours of daylight for this date
    """
    def get_day_light_length(self):
        stateJson = self.get_weather_data()
        sunrise_time = stateJson["sunrise"]
        sunset_time = stateJson["sunset"]
        FMT = '%H:%M:%S'
        diff = datetime.strptime(sunset_time, FMT) - datetime.strptime(sunrise_time, FMT)
        hours = diff.total_seconds()/3600
        return hours

    # to be acquired through API
    def get_solar_insolation(self, solar_insolation):
        pass

    """ 
    Returns array list of cloud cover percentage for the day
    Output:
        array list [0..23] with the cloud cover value at the hour index
    """
    def get_cloud_cover(self):

        stateJson = self.get_weather_data()
        hourly_history = stateJson["hourlyWeatherHistory"]
        cc_per_hour = []
        for x in range(0,len(hourly_history)):
            cc_per_hour.append(hourly_history[x]["cloudCoverPct"])
        return cc_per_hour

    def calculate_solar_energy(self):
        pass

    def get_state_id(self):
        """Get state id for any state code"""
        state = str(self.post_code)
        requestURL = "http://118.138.246.158/api/v1/location?postcode="+state
        response = requests.get(requestURL)
        stateJson = response.json()
        properties = stateJson[0]
        return properties["id"]

    def get_weather_data(self):
        """Get json for state and  date from api"""
        start_date = datetime.strftime(self.start_datetime,"%Y-%m-%d")
        state_id = self.get_state_id()
        requestURL = "http://118.138.246.158/api/v1/weather?location=" + state_id + "&date=" + start_date
        response = requests.get(requestURL)
        return response.json()


if __name__ == '__main__':
        calculator = Calculator("82", "20", "80", "21/09/2021", "14:30", "5", "3168")
        print(calculator.get_solar_energy_duration())
