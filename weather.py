#!/usr/bin/env python3

import urllib.request, json
from datetime import datetime

class Weather:
    '''Class to handle retrieving json data from forecast.io'''
    def __init__(self, api_key, latitude, longitude, units='si'):
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.units = units

    def retrieve_forecast(self, day):
        '''Retrieve forecast dictionary data for day'''
        url = 'https://api.forecast.io/forecast/{0.api_key}/{0.latitude},{0.longitude},{1}T00:00:00?units={0.units}'.format(self, day)
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        forecast = json.loads(content)

        return forecast

    def retrieve_weather_by_hour(self, forecast):
        '''Returns dictionary of hours between 0 and 23 for the day that contain dictionaries of weather metrics'''

        hourly_weather = {}
        for each_hour_data in forecast['hourly']['data']:
            date_time = datetime.fromtimestamp(each_hour_data['time'])
            del each_hour_data['time'], each_hour_data['icon'], each_hour_data['summary']
            hourly_weather[date_time.hour] = each_hour_data

        return hourly_weather

    def retrieve_weather_from_day(self, forecast):
        ''' Retrieve dictionary of weather metrics for the day '''
        return forecast['daily']['data'][0]

    def summarise_night_day(self, hourly_weather, summary_function):
        '''Summarise 7 hours of weather from the night before and during the day'''
        night_hours = [0,1,2,3,4,5,6]
        day_hours = [9,10,11,12,13,14,15]

        night_day_weather = {'night': [hourly_weather[hour] for hour in night_hours],
                            'day': [hourly_weather[hour] for hour in day_hours]}

        night_day_list_metrics = {'night': {},'day': {}}

        for time in night_day_weather.keys():
            for each_hour in night_day_weather[time]:
                for metric in each_hour.keys():
                    if metric in night_day_list_metrics[time].keys():
                        night_day_list_metrics[time][metric].append(each_hour[metric])
                    else:
                        night_day_list_metrics[time][metric] = [each_hour[metric]]

        night_day_metric_summary = {'night': {},'day': {}}

        for time in night_day_list_metrics.keys():
            for metric in night_day_list_metrics[time].keys():
                try:
                    summary_value = summary_function(night_day_list_metrics[time][metric])
                except:
                    string_freq_dict = {}
                    summary_value = None
                    for string in night_day_list_metrics[time][metric]:
                        if string in string_freq_dict.keys():
                            string_freq_dict[string] += 1
                            if string_freq_dict[string] > string_freq_dict[summary_value]:
                                summary_value = string
                        else:
                            string_freq_dict[string] = 1
                            if summary_value is None:
                                summary_value = string

                night_day_metric_summary[time][metric] = summary_value

        return (night_day_metric_summary['night'], night_day_metric_summary['day'])

def main():
    pass

if __name__ == "__main__":
    main()
