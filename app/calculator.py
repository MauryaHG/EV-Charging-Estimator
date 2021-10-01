import math

import datetime as datetime
import holidays
import requests
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta


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
        #self.solar_charging_time = self.get_solar_charging_time()

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
        print(aus_state_holidays)
        return self.start_datetime in aus_state_holidays

    def is_weekday(self):
        """Check if the charging start date is a weekday"""
        return self.start_datetime.weekday() <= 4

    def is_peak(self):
        """Check if the charging start time is during peak hours"""
        lower_bound = datetime.strptime(str(self.start_datetime.date()) + ' 06:00', '%Y-%m-%d %H:%M')
        upper_bound = datetime.strptime(str(self.start_datetime.date()) + ' 18:00', '%Y-%m-%d %H:%M')
        return lower_bound <= self.start_datetime <= upper_bound

    def calculate_cost(self):
        date_now = datetime.now()
        start_date = self.start_datetime
        time = self.start_datetime
        if start_date < date_now:
            timedates = self.get_charging_times(start_date)
            print(timedates)
            for timedate in timedates:
                self.calculate_cost_hour(timedate)
        else:
            past_dates = self.get_ref_dates(start_date)
            print(past_dates)
            for date_time in past_dates:
                print(date_time)
                print(self.get_charging_times(date_time))

    def get_ref_dates(self, date):
        while date > datetime.now():
            ref_dates = [date + relativedelta(years=-1), date + relativedelta(years=-2), date + relativedelta(years=-3)]
            date = date + relativedelta(years=-1)
        return ref_dates

    def get_charging_times(self, date):
        """ Get the charging times from start to finish"""
        start_datetime = date
        date = start_datetime.date()
        charging_time = self.time_calculation()/60
        print(charging_time)
        times = []
        hour = start_datetime.time()
        mins = (60 - start_datetime.minute) / 60
        times.append([date, hour, mins])

        for i in range(1, math.trunc(charging_time)):
            date_time = (start_datetime + timedelta(hours=i * 1))
            hour = date_time.time()
            date = date_time.date()
            times.append([date, hour, 1])

        timedate = (start_datetime + timedelta(hours=math.trunc(charging_time), minutes=(charging_time % 1)*60))
        time = timedate.time()
        mins = (60 - timedate.minute) / 60
        date = timedate.date()
        times.append([date, time, mins])
        return times

    def is_holiday_p_hour(self, timedata):
        """Check if this date is a holiday"""
        self.is_holiday()
        sate = self.get_state_code()
        aus_state_holidays = holidays.CountryHoliday('AUS', prov=sate, state=None)
        print(aus_state_holidays)
        return timedata[0] in aus_state_holidays

    def is_weekday_p_hour(self, timedate):
        """Check if the this date is a weekday"""
        return timedate[0].weekday() <= 4
    def is_peak_p_hour(self, timedate):
        """Check if this time peak hour"""
        FMT = '%H:%M:%S'
        lower = datetime.strptime("06:00:00", FMT).time()
        upper = datetime.strptime("18:00:00", FMT).time()
        return lower <= timedate[1] <= upper

    def calculate_cost_hour(self, timedate):
        print(timedate)
        print(self.is_holiday_p_hour(timedate))
        print(self.is_weekday_p_hour(timedate))
        if self.is_holiday_p_hour(timedate) or self.is_weekday_p_hour(timedate):
            surcharge_factor = 1.1
        else:
            surcharge_factor = 1
        if self.is_peak_p_hour(timedate):
            discount_factor = 1
        else:
            discount_factor = 0.5
        if self.is_during_sun_hours(timedate):
            self.get_price_and_power()
            dl = self.get_day_light_length(timedate[0])
            si = self.get_sun_hour(timedate[0])
            solar_energy = si * (timedate[2]/dl) * 50 * 0.2
            charge_energy = self.power * timedate[2]
            net_energy = charge_energy - solar_energy
            if net_energy < 0:
                net_energy = 0
            cost = (self.final_charge - self.initial_charge) / 100 * net_energy * self.base_price / 100 * surcharge_factor * discount_factor
        else:
            charge_energy = self.power * timedate[2]
            cost = (self.final_charge - self.initial_charge) / 100 * charge_energy * self.base_price / 100 * surcharge_factor * discount_factor

        return cost

    def is_during_sun_hours(self, timedata):
        date = timedata[0]
        time = timedata[1]
        stateJson = self.get_weather_data(date)
        FMT = '%H:%M:%S'
        sunrise_time = datetime.strptime(stateJson["sunrise"], FMT)
        sunset_time = datetime.strptime(stateJson["sunset"], FMT)
        if sunrise_time.time() <= time <= sunset_time.time():
            return True
        else:
            return False

    def get_sun_hour(self, date):
        """ Get sunhours(solar isolation for a specific date in a state)"""
        stateJson = self.get_weather_data(date)
        return stateJson["sunHours"]

    def get_solar_energy_duration(self, date):
        """ returns total hours of solar generation in hours while charging"""
        start_time = self.start_datetime
        weather_data = self.get_weather_data(date)
        FMT = '%H:%M:%S'
        sunrise_time = datetime.strptime(weather_data["sunrise"], FMT)
        sunset_time = datetime.strptime(weather_data["sunset"], FMT)
        charging_time = timedelta(minutes=self.time_calculation())
        final_time = self.start_datetime + charging_time
        print(sunrise_time)
        print(sunset_time)
        print(start_time)
        print(final_time.time())
        if start_time.time() < sunrise_time.time() and final_time <= sunset_time:
            du = (final_time - sunrise_time)
            print("1")
        elif start_time.time() >= sunrise_time.time() and final_time.time() <= sunset_time.time():
            du = charging_time
            print("2")
        elif start_time.time() >= sunrise_time.time() and final_time.time() > sunset_time.time():
            du = sunset_time - start_time
            print("3")
        elif start_time.time() < sunrise_time.time() and final_time.time() > sunset_time.time():
            du = self.get_day_light_length()
            print("4")
        print(du)
        return du.seconds / 3600

    """ 
     Returns  day light hours for a specific date in a state
     Output:
         float of hours of daylight for this date
    """

    def get_day_light_length(self, date):
        stateJson = self.get_weather_data(date)
        sunrise_time = stateJson["sunrise"]
        sunset_time = stateJson["sunset"]
        FMT = '%H:%M:%S'
        diff = datetime.strptime(sunset_time, FMT) - datetime.strptime(sunrise_time, FMT)
        hours = diff.total_seconds() / 3600
        return hours

    """ 
    Returns array list of cloud cover percentage for the day
    Output:
        array list [0..23] with the cloud cover value at the hour index
    """

    def get_cloud_cover(self, date):

        stateJson = self.get_weather_data(date)
        hourly_history = stateJson["hourlyWeatherHistory"]
        cc_per_hour = []
        for x in range(0, len(hourly_history)):
            cc_per_hour.append(hourly_history[x]["cloudCoverPct"])
        return cc_per_hour

    def calculate_solar_energy(self):
        """ Get solar energy generated """
        date = datetime.strftime(self.start_datetime, "%Y-%m-%d")
        si = self.get_sun_hour(date)
        dl = self.get_day_light_length(date)
        du = self.get_solar_energy_duration(date)
        e = si * (du / dl) * 50 * 0.2
        return e

    def calculate_solar_energy_future(self, date):
        ref_dates = self.get_ref_dates(date)
        total = [0] * 3
        index = 0
        for i in ref_dates:
            total[index] = self.calculate_solar_energy_w_cc(str(i))
            index += 1
        return total


    def get_solar_charging_time(self):
        start_datetime = self.start_datetime
        date = self.start_datetime.date()
        solar_du = self.get_solar_energy_duration(str(date))
        times = []
        hour = start_datetime.hour
        mins = start_datetime.minute / 60
        times.append([date, hour, mins])

        for i in range(1, math.trunc(solar_du)):
            date_time = (start_datetime + timedelta(hours=i * 1))
            hour = date_time.hour
            date = date_time.date()
            times.append([date, hour, 1])

        time = (start_datetime + timedelta(hours=math.trunc(solar_du), minutes=solar_du % 1))
        hour = time.hour
        mins = time.minute / 60
        date = time.date()
        times.append([date, hour, mins])
        return times

    def calculate_solar_energy_w_cc(self, date):
        """ Get solar energy generated with cloud cover"""
        this_date = date[0]
        hour = date[1]
        du = date[2]
        si = self.get_sun_hour(str(this_date))
        dl = self.get_day_light_length(str(this_date))
        cc_list = self.get_cloud_cover(str(this_date))
        cc = cc_list[hour]
        e = si * (du / dl) * (1 - (cc / 100)) * 50 * 0.2
        return e



    def get_solar_charges(self):
        times = self.solar_charging_time
        solar_charge = []
        for time in times:
            solar_charge.append(self.calculate_solar_energy_w_cc(time))
        return solar_charge

    def get_state_id(self):
        """Get state id for any state code"""
        state = str(self.post_code)
        requestURL = "http://118.138.246.158/api/v1/location?postcode=" + state
        response = requests.get(requestURL)
        if response.status_code == 200:
            stateJson = response.json()
            properties = stateJson[0]
            return properties["id"]

    def get_state_code(self):
        """Get state id for any state code"""
        state = str(self.post_code)
        requestURL = "http://118.138.246.158/api/v1/location?postcode=" + state
        response = requests.get(requestURL)
        if response.status_code == 200:
            stateJson = response.json()
            properties = stateJson[0]
            return properties["state"]

    def get_weather_data(self, *date):
        """Get json for state and  date from api"""

        if len(date) == 0:
            start_date = datetime.strftime(self.start_datetime, "%Y-%m-%d")
        else:
            print("date")
            print(date)
            print(date[0])
            start_date = str(date[0])
            print(start_date[0])
        state_id = self.get_state_id()
        requestURL = "http://118.138.246.158/api/v1/weather?location=" + state_id + "&date=" + start_date
        response = requests.get(requestURL)
        return response.json()

    def is_holiday_(self, date):
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

    def req2(self):
        start_date = self.start_datetime
        timedates = self.get_charging_times(start_date)
        cost_arr = [0 for _ in range(len(timedates))]
        for i in range(0, len(timedates)):
            cost_arr[i] = self.calculate_cost_hour(timedates[i])
        total_cost = 0
        for j in range(0, len(cost_arr)):
            total_cost += cost_arr[i]
        return total_cost


if __name__ == '__main__':
    calculator = Calculator("100", "85", "100", "28/09/2020", "17:15", "1", "3800")
    print(calculator.calculate_cost())


