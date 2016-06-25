#!/usr/bin/env python3

import os
import numpy as np

from weather import Weather
from logdata import LogData


def main():
    dates = ['2015-06-20', '2015-06-21', '2015-06-22', '2015-06-23', '2015-06-24']
    api_key = os.environ.get("WEATHER_API_KEY", None)
    latitude, longitude = (-35.280317, 149.111644)

    weather = Weather(api_key, latitude, longitude, units='si')
    logger = LogData()

    for each_date in dates:
        forecast = weather.retrieve_forecast(each_date)

        weather_whole_day = weather.retrieve_weather_from_day(forecast)
        hourly_weather = weather.retrieve_weather_by_hour(forecast)
        weather_6_am = hourly_weather[6]

        night_weather, day_weather = weather.summarise_night_day(hourly_weather, np.mean)

        logger.log_output(weather_whole_day, each_date, 'daily')
        logger.log_output(weather_6_am, each_date, 'hourly', 6)
        logger.log_output(night_weather, each_date, 'night')
        logger.log_output(day_weather, each_date, 'day')


    logger.write_output('test.csv')

if __name__ == "__main__":
    main()
