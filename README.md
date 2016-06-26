# Forecast
A package for retrieving daily weather data using the [forecast.io](http://forecast.io/) API. Uses the [NumPy](http://www.numpy.org/) and [pandas](http://pandas.pydata.org/) packages.

I wrote this as part of my PhD analysing honeybee behaviour and thought I'd give this code it's own package so I could reuse it later for other projects.

An example program using the package is [available here](example.py).

## Weather Class

You initialise the class with the API key available for free from [here](https://developer.forecast.io/), the latitude and longitude of the location you're interested in and optionally the units the data should be in (defaults to metric, but you can pass 'us' to receive imperial).

You can now use the weather object to retrieve weather data for different dates.

```python
api_key = 'mykeystring'
latitude, longitude = (-35.280317, 149.111644)
weather = Weather(api_key, latitude, longitude, units='si')

date = '2015-06-20'
forecast = weather.retrieve_forecast(date)
```

You can use 3 methods now to get different weather data from the day:

```python

weather_whole_day = weather.retrieve_weather_from_day(forecast)

hourly_weather = weather.retrieve_weather_by_hour(forecast)
weather_6_am = hourly_weather[6]

night_weather, day_weather = weather.summarise_night_day(hourly_weather, np.mean)
```

1. `retrieve_weather_from_day`: Returns a dictionary with data on different weather metrics throughout the day.
2. `retrieve_weather_by_hour`: Returns a dictionary with keys for every hour of the day ranging from 0-23. Each hour contains a dictionary with data about the weather during that time.
3. `summarise_night_day`: Takes 7 hours during the night before and 7 hours during the day and generates a summary metric for all the weather data in those time periods. This summary metric is determined by the function you pass this method. It returns a tuple containing these summary metrics for night and day.

## LogData Class

The LogData class stores the output from the previous 3 methods discussed above. You pass it the dictionary containing the weather data for that time period, the date, the name for the time period the data comes from and (optionally) the hour that the data came from.

You can then write out the data as a csv file when you're done.

```python
logger = LogData()

logger.log_output(weather_whole_day, date, 'daily')
logger.log_output(weather_6_am, date, 'hourly', 6)
logger.log_output(night_weather, date, 'night')
logger.log_output(day_weather, date, 'day')

logger.write_output('test.csv')
```
