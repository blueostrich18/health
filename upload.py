# https://pyshark.com/google-sheets-api-using-python/#creating-google-api-credentials
# https://docs.gspread.org/en/latest/user-guide.html#getting-a-cell-value

from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date, timedelta
from time import sleep
import gspread
import mfphelper
import whoophelper
import json
import sys
import argparse
import configparser
import fitbithelper
import traceback

def updateFitBitData(login, day, date, map, worksheet, use_whoop_data="yes"):
    data = fitbithelper.getFBDiary( 
        login,
        date.year,
        date.month,
        date.day,
    )
    for entry in data:
        if not use_whoop_data == "no" and not entry == "steps":
            continue
        try:
            coord = map[day][0]["fitbit"][entry]
            worksheet.update(coord, data[entry])
        except:
            print("Failed fitbit")
            traceback.print_exc()

def updateMFPData(login, day, date, map, worksheet, config):
    diary = mfphelper.getMFPDiary(
        login,
        date.year,
        date.month,
        date.day,
    )
    # print(diary)
    for entry in diary:
        # print(entry)
        try:
            coord = map[day][0]["mfp"][entry]
            if entry == "water":
                diary[entry] = round(float(diary[entry]) / 1000, 2)
            worksheet.update(coord, diary[entry])
        except:
            traceback.print_exc()


def updateWhoopData(login, day, date, map, worksheet ):
    data = whoophelper.getWhoopData( login, date, date)
    # print(data)
    for entry in data:
        try:
            coord = map[day][0]["whoop"][entry]
            worksheet.update(coord, data[entry])
        except:
            traceback.print_exc()


def checkIfComplete(worksheet, map):
    if worksheet.acell(map["complete"]).value == "Y":
        return True
    else:
        return False


def getMap(path):
    return json.load(open(path, "r"))


def authToSheets(creds):
    return gspread.service_account(filename=creds)


def openSheet(gc, url):
    return gc.open_by_url(url)


def openTab(sheet, tab_name):
    return sheet.worksheet(tab_name)


def getDateRange(start, end):
    # end = datetime.strptime(end, "%Y-%m-%d")
    # start = datetime.strptime(start, "%Y-%m-%d")
    delta = end - start
    dates = []
    for i in range(delta.days + 1):
        day = start + timedelta(days=i)
        dates.append(day)
    return dates


def main(args):
    ini = "health.ini"
    config = configparser.ConfigParser()
    config.read(ini)
    tab_name = args.sheet

    map = getMap(config["gsheet"]["json"])
    gc = authToSheets(config["gsheet"]["creds"])
    gsheet = openSheet(gc, config["gsheet"]["url"])
    worksheet = openTab(gsheet, tab_name)

    if checkIfComplete(worksheet, map):
        print(
            "!!!!This tab/worksheet is marked as complete!!!! Exiting to protect the data."
        )
        sys.exit()

    start = args.start
    end = args.end
    dates = getDateRange(start, end)

    day = args.sday
    login = mfphelper.login(config["mfp"]["username"], config["mfp"]["password"])
    for date in dates:
        try:
            updateMFPData(login, str(day), date, map, worksheet, config)
        except:
            print("Failed to Update MFP data")
        day += 1

    day = args.sday
    login = whoophelper.login(ini)
    for date in dates:
        try:
            updateWhoopData(login, str(day), str(date), map, worksheet)
        except:
            print("Failed to Update Whoop data")
        day += 1

    day = args.sday
    login = fitbithelper.login(config['fitbit']['client_id'],
        config['fitbit']['client_secret'],
        config['fitbit']['uri'])
    for date in dates:
        try:
            updateFitBitData(
                login, 
                str(day), 
                date, 
                map, 
                worksheet, 
                use_whoop_data=config['fitbit']['use_whoop_data'])
        except:
            print("Failed to Update Fitbit data")
            traceback.print_exc()
            
        day += 1



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-sheet",
        type=str,
        required=True,
        help="The name of the sheet/tab, you would like insert data into. (week1)",
    )
    parser.add_argument(
        "-start",
        required=True,
        type=date.fromisoformat,
        help="Date to start pulling data from MFP and Whoop. (2021-12-29)",
    )
    parser.add_argument(
        "-end",
        required=True,
        type=date.fromisoformat,
        help="Date to end pulling data from MFP and Whoop. (2021-12-30)",
    )
    parser.add_argument(
        "-sday",
        type=int,
        default=1,
        choices=[1, 2, 3, 4, 5, 6, 7],
        help="The day of the week that you would like start filling data out on. 1 is the default but you can choose 1-7.",
    )
    args = parser.parse_args()
    main(args)


# setup variables
# package
# post to github
