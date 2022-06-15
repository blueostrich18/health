# MFP and Whoop data into Google sheet
## Tool to get MyFitnessPal(MFP) and Whoop data into a google sheet

This tool utilizes the work of https://github.com/coddingtonbear/python-myfitnesspal/ and https://github.com/irickman/whoop-downloader

Follow these instructions for setting up Google API Service Account: https://support.google.com/a/answer/7378726

***You must share the google sheet you are putting data into with the service account you just created in the step above. Service account email can be found in the json cred file that was downloaded***

Highly recommended to run in a [python virtual enviornment](https://docs.python.org/3/library/venv.html)

```python
pip install -r requirements.txt
```

Make sure you have your Whoop and MFP creds available

Add your data to the health.ini file
```INI
[whoop]
username=
password=

[gsheet]
json=path\to\spreadsheet_map.json
creds={location of json file
url={url of google sheet}

[mfp]
username=
password=

[fitbit]
client_id={get from dev.fitbit.com}
client_secret={get from dev.fitbit.com}
uri={Must be HTTPS and the same as the one used when setting up the app in dev.fitbit.com}
use_whoo_data={yes if you prefer to use the whoop data for RHR, HVR, and sleep}
``` 

Configure your spreadsheet_map.json to match the layout of your spreadsheet. This is how the program knows what data goes in what cells.

Usage
```bash
usage: upload.py [-h] -sheet SHEET -start START -end END [-sday {1,2,3,4,5,6,7}]

optional arguments:
  -h, --help            show this help message and exit
  -sheet SHEET          The name of the sheet/tab, you would like insert data into. (week1)
  -start START          Date to start pulling data from MFP and Whoop. (2021-12-29)
  -end END              Date to end pulling data from MFP and Whoop. (2021-12-30)
  -sday {1,2,3,4,5,6,7} The day of the week that you would like start filling data out on. 
                        1 is the default but you can choose 1-7.
```

```bash
python upload.py -sheet "Week1" -start "2021-12-27" -end "2021-12-29"
```

## Fitbit 
Installation of the python fitbit modules is required but will need to be modified. Also HTTPS is required by Fitbit. Create a private key and a cert. To setup the fitbit app dev follow https://towardsdatascience.com/collect-your-own-fitbit-data-with-python-ff145fa10873

Next you will need to modify the Python FitBit module by editing the file api.py, for me located /Users/<username>/Library/Python/3.9/lib/python/site-packages/fitbit/api.py.
Modify apy.py to add 'hrv' to the RESOURCE_LIST
```python
 190     API_ENDPOINT = "https://api.fitbit.com"
 191     API_VERSION = 1
 192     WEEK_DAYS = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']
 193     PERIODS = ['1d', '7d', '30d', '1w', '1m', '3m', '6m', '1y', 'max']
 194 
 195     RESOURCE_LIST = [
 196         'body',
 197         'activities',
 198         'foods/log',
 199         'foods/log/water',
 200         'sleep',
 201         'heart',
 202         'bp',
 203         'glucose',
 204         'hrv',
 205     ]
```
