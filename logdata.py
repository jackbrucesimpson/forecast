#!/usr/bin/env python3

import numpy as np
import pandas as pd

class LogData:
    '''Handles missing data while logging and writing output'''
    def __init__(self):
        self.output = {'date':[], 'hour':[], 'time_period':[]}

    def log_output(self, weather_metrics, date, time_period, hour=np.nan):
        '''Checks for missing data as it takes dictionary of weather metrics, date and time period (hour is optional) and adds it to output dictionary'''
        self.output['date'].append(date)
        self.output['time_period'].append(time_period)
        self.output['hour'].append(hour)

        for metric in weather_metrics.keys():
            if metric in self.output.keys():
                self.output[metric].append(weather_metrics[metric])
            else:
                self.output[metric] = [np.nan] * (len(self.output['time_period']) - 1)
                self.output[metric].append(weather_metrics[metric])

        metrics_to_update = set(self.output.keys()) - set(weather_metrics.keys())
        for metric in metrics_to_update:
            self.output[metric].extend((len(self.output['date']) - len(self.output[metric])) * [np.nan])

        return None

    def write_output(self, path_filename):
        '''Checks for missing data and then writes output to csv'''
        for column in self.output.keys():
            if len(self.output[column]) < len(self.output['date']):
                self.output[column].extend((len(self.output['date']) - len(self.output[column])) * [np.nan])

        if not path_filename.endswith('csv'):
            path_filename += '.csv'

        output_df = pd.DataFrame(self.output)
        output_df.to_csv(path_filename, index=False)

def main():
    pass

if __name__ == "__main__":
    main()
