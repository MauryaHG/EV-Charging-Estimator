import math

import datetime as datetime
from os import truncate

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
        charging_time = (((self.final_charge - self.initial_charge) / 100 * self.battery_capacity) / self.power) * 60
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
            charging_cost += (
                                     self.final_charge - self.initial_charge) / 100 * self.battery_capacity * self.base_price / 100 * surcharge_factor * discount_factor * time_factor
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

    """Calculate the cost for charging considering all dates and solar charging 
    with cloud cover if applicable
    Output: Total cost to 2dp
    """

    def calculate_cost_alg3(self):
        date_now = datetime.now()
        start_date = self.start_datetime
        total_cost = 0
        # if date is in the past
        if start_date < date_now:
            timedates = self.get_charging_times(start_date)
            # get cost for each partial/whole hour
            for timedate in timedates:
                total_cost += self.calculate_cost_hour(timedate, True)
        # if date is in the future
        else:
            # get dates of past 3 years
            past_dates = self.get_ref_dates(start_date)
            # for each date calculate
            for date_time in past_dates:
                cost = 0
                # get cost for each partial/whole hour
                timedates = self.get_charging_times(date_time)
                for timedate in timedates:
                    cost += self.calculate_cost_hour(timedate, True)
                # add cost of all years
                total_cost += cost
            # get average cost
            total_cost = total_cost / 3
        return total_cost

    """
    Calculate the cost of charging for the given hour
    Input
        timedate:array with date[0] and time[1] and charging period date[2]
        cloudcover: default false,if true then cloud cover taken into solar energy calculation
    Output
        cost: cost for charging for this hour
    """

    def calculate_cost_hour(self, timedate, cloudcover=False):
        """
        Function for calculating cost of charging for a single hour during the charging period. Checks if it is currently
        a holiday/weekday and if it is peak/off-peak hour and if there is daylight. If there is daylight solar energy is generated
        and subtracted from charging energy to find net energy which is then used to calculatae the cost for that hour.
        The function also works when a partial hour is inputted, ie 0.5 or 0.25 instead of 1.
        """
        # is cloudcover is true get cloudcover value for this day

        # check if this date is a holiday or a weekday
        if self.is_holiday_p_hour(timedate) or self.is_weekday_p_hour(timedate):
            surcharge_factor = 1.1
        else:
            surcharge_factor = 1
        # check if this hour is a peak hour
        if self.is_peak_p_hour(timedate):
            discount_factor = 1
        else:
            discount_factor = 0.5
        # if this hour has sun light
        if self.is_during_sun_hours(timedate):
            if cloudcover:
                cc_value = self.get_cloud_cover(timedate)
            else:
                cc_value = 0
            # initialise  price and power
            self.get_price_and_power()
            dl = self.get_day_light_length(timedate)  # get daylight duration
            si = self.get_sun_hour(timedate)  # get solar isolation
            solar_energy = si * (timedate[2] / dl) * (1 - (cc_value / 100)) * 50 * 0.2  # calculate solar energy
            charge_energy = self.power * timedate[2]
            # get charge for this charge duration
            net_energy = charge_energy - solar_energy
            # if net charge is less than 0 then set it to 0
            if net_energy < 0:
                net_energy = 0
            # calculate cost for this charge duration
            cost = net_energy * (self.base_price / 100) * surcharge_factor * discount_factor
        else:
            charge_energy = self.power * timedate[2]
            # calculate cost for this charge duration
            cost = charge_energy * (self.base_price / 100) * surcharge_factor * discount_factor
        return cost

    def is_holiday_p_hour(self, timedata):
        """Check if this date is a holiday"""
        sate = self.get_state_code()
        aus_state_holidays = holidays.CountryHoliday('AUS', prov=sate, state=None)
        return timedata[0] in aus_state_holidays

    @staticmethod
    def is_weekday_p_hour(timedate):
        """Check if the this date is a weekday"""
        return timedate[0].weekday() <= 4

    @staticmethod
    def is_peak_p_hour(timedate):
        """Check if this time peak hour"""
        time = timedate[1]
        FMT = '%H:%M:%S'
        lower = datetime.strptime("06:00:00", FMT).time()
        upper = datetime.strptime("18:00:00", FMT).time()
        return lower <= time <= upper

    def is_during_sun_hours(self, timedate):
        """Check if this time is during sun hours"""
        time = timedate[1]
        stateJson = self.get_weather_data(timedate)
        FMT = '%H:%M:%S'
        sunrise_time = datetime.strptime(stateJson["sunrise"], FMT)
        sunset_time = datetime.strptime(stateJson["sunset"], FMT)

        if sunrise_time.time() <= time <= sunset_time.time():
            return True
        else:
            return False

    @staticmethod
    def get_ref_dates(date):
        """Get dates 3 years behind of current year with specified date """
        ref_dates = date
        while date > datetime.now():
            ref_dates = [date + relativedelta(years=-1), date + relativedelta(years=-2), date + relativedelta(years=-3)]
            date = date + relativedelta(years=-1)
        return ref_dates

    def get_charging_times(self, date):
        """ Get the charging times from start to finish"""
        start_datetime = date
        date = start_datetime.date()
        charging_time = self.time_calculation() / 60
        times = []
        final_time = (start_datetime + timedelta(hours=charging_time))
        ad_min_time = (start_datetime + timedelta(hours=(charging_time % 1)))
        # if charging is over multiple hour periods
        if charging_time > 1 or ad_min_time.hour > start_datetime.hour:
            # get charging duration

            hour = start_datetime.time()
            mins = (60 - start_datetime.minute) / 60
            times.append([date, hour, mins])  # append first parial hour

            # append all whole hours
            for i in range(1, math.trunc(charging_time)):
                date_time = (start_datetime + timedelta(hours=i * 1))
                hour = date_time.time()
                date = date_time.date()
                times.append([date, hour, 1])
            # add mins in charging duration and add to array
            timedate = (start_datetime + timedelta(hours=math.trunc(charging_time), minutes=(charging_time % 1) * 60))
            time = timedate.time()
            mins = (timedate.minute) / 60
            date = timedate.date()
            times.append([date, time, mins])
        else:
            hour = final_time.time()
            mins = charging_time
            times.append([date, hour, mins])
        return times

    def get_sun_hour(self, timedate):
        """ Get sunhours(solar isolation for a specific date in a state)"""
        stateJson = self.get_weather_data(timedate)
        return stateJson["sunHours"]

    def get_day_light_length(self, timedate):
        """
        Returns  day light hours for a specific date in a state
        Output:
             float of hours of daylight for this date
        """
        stateJson = self.get_weather_data(timedate)
        sunrise_time = stateJson["sunrise"]
        sunset_time = stateJson["sunset"]
        FMT = '%H:%M:%S'
        diff = datetime.strptime(sunset_time, FMT) - datetime.strptime(sunrise_time, FMT)
        hours = diff.total_seconds() / 3600
        return hours

    def get_cloud_cover(self, timedate):
        """
        Returns array list of cloud cover percentage for the day
        Output:
            array list [0..23] with the cloud cover value at the hour index
        """
        weatherJson = self.get_weather_data(timedate)
        hourly_history = weatherJson["hourlyWeatherHistory"]
        time = timedate[1]
        this_hour = hourly_history[time.hour]
        cc = this_hour["cloudCoverPct"]
        return cc

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
            start_date = str(self.start_datetime.date())
        else:
            if type(date[0]) == str:
                start_date = date[0]
            else:
                start_date = str(date[0][0])
        state_id = self.get_state_id()
        requestURL = "http://118.138.246.158/api/v1/weather?location=" + state_id + "&date=" + start_date
        response = requests.get(requestURL)
        return response.json()

    def req2(self):
        """
        Function for calculating the cost of charging for REQ2 of the assignment. The function creates a list of lists
        that contains the date hours and minutes seperated. Using a for loop a single hour is selected and passed on to
        calculate_cost_hours method to calculate the cost of charging for a single hour as specified in ALG2. Each value
        is stored and at the end all the values are added and returned.
        """
        start_date = self.start_datetime
        timedates = self.get_charging_times(start_date)
        cost_arr = [0 for _ in range(len(timedates))]
        for i in range(0, len(timedates)):
            cost_arr[i] = self.calculate_cost_hour(timedates[i])
        total_cost = 0
        for j in range(0, len(cost_arr)):
            total_cost += cost_arr[j]
        return total_cost


if __name__ == '__main__':
    pass
