# https://github.com/irickman/whoop-downloader

from whoop_download import whoop_login
from math import floor
import pandas


def login(file):
    client = whoop_login()
    client.get_authorization(file)
    return client


def getWhoopData(client, start_date, end_date):
    keydata = client.get_keydata_timeframe(start=start_date, end=end_date)

    resting_hr = keydata["recovery.restingHeartRate"]
    sleep = keydata["sleep.sleeps"].values.tolist()[0]

    sleep_efficiency = round(float(sleep[0]["sleepEfficiency"]), 2)

    datadict = keydata.to_dict()

    HRV = int(round(float(datadict["recovery.heartRateVariabilityRmssd"][0]) * 1000, 0))

    qualitySleep = float(datadict["sleep.qualityDuration"][0])
    hours = int(floor(qualitySleep / 60))
    mins = int(round(qualitySleep % 60, 0))
    sleep_duration = '{}:{:02d}'.format( hours,mins)

    # print(datadict)

    return {
        "sleep_duration": sleep_duration or 0,
        "sleep_effeciency": sleep_efficiency or 0,
        "HRV": HRV or 0,
        "RHR": int(resting_hr[0]) or 0,
        "strain": round(datadict["strain.score"][0], 1) or 0,
        "recovery": datadict["recovery.score"][0] or 0,
    }


# getWhoopData(login(), "2021-12-22", "2021-12-22")
