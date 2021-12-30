# https://pyshark.com/google-sheets-api-using-python/#creating-google-api-credentials
# https://docs.gspread.org/en/latest/user-guide.html#getting-a-cell-value

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import mfphelper
import whoophelper
import json
from datetime import datetime, date, timedelta
import sys
import argparse
import configparser


def updateMFPData(day, date, map, worksheet, config):
    diary = mfphelper.getMFPDiary(
        mfphelper.login(config["mfp"]["username"], config["mfp"]["password"]),
        date.year,
        date.month,
        date.day,
    )
    # print(diary)
    for entry in diary:
        # print(entry)
        coord = map[day][0]["mfp"][entry]
        if entry == "water":
            diary[entry] = round(float(diary[entry]) / 1000, 2)
        worksheet.update(coord, diary[entry])


def updateWhoopData(day, date, map, worksheet, whoop_creds):
    data = whoophelper.getWhoopData(whoophelper.login(whoop_creds), date, date)
    # print(data)
    for entry in data:
        # print(entry)
        coord = map[day][0]["whoop"][entry]
        worksheet.update(coord, data[entry])


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
    for date in dates:
        updateMFPData(str(day), date, map, worksheet, config)
        updateWhoopData(str(day), str(date), map, worksheet, ini)
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
