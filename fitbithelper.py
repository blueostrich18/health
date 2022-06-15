#!/usr/bin/env python3
# https://shanelynn.ie/plot-your-fitbit-data-in-python-api-v1-2

import fitbit
import gather_keys_oauth2 as Oauth2
import datetime

def login(client_id, client_secret, uri):
    server = Oauth2.OAuth2Server(client_id, client_secret, redirect_uri=uri)
    server.browser_authorize()
    return server

def getFBDiary(server, year, month, day):
    fitbit_data = { "sleep_duration":None, "sleep_efficiency":None,"steps":0,"HRV":0,"RHR":0}
    date = "{:04d}-{:02d}-{:02d}".format(year, month, day)
    sleep_data = server.fitbit.sleep(date)
    tmp = sleep_data['summary']['totalMinutesAsleep']
    fitbit_data["sleep_duration"] = '{:02d}:{:02d}'.format(*divmod(tmp, 60) )
    fitbit_data["sleep_efficiency"] = sleep_data['sleep'][0]['efficiency']/100

    activities = server.fitbit.activities(date)
    fitbit_data['steps'] = activities['summary']['steps']
    fitbit_data['RHR'] = activities['summary']['restingHeartRate']
    hrv = server.fitbit.hrv(date)
    fitbit_data['HRV'] = hrv['hrv'][0]['value']['dailyRmssd']
    return fitbit_data
