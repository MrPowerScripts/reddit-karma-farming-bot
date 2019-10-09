import gspread
import subprocess
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
num = 0
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

gc = gspread.authorize(credentials)

sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1XR3V8mkOcsskDF66jvC0rBrj6KyhepHY4ZXj273w2Qo/edit#gid=0')

sheet = sh.get_worksheet(0)

list_of_lists = sheet.get_all_values()


for list in list_of_lists:
    PROXY = (list[0])
    REDDIT_CLIENT_ID = (list[1])
    REDDIT_SECRET = (list[2])
    REDDIT_USERNAME = (list[3])
    REDDIT_PASSWORD = (list[4])
    REDDIT_USER_AGENT = (list[5])
try:
    subprocess.Popen(["source venv/bin/activate &&","python2.7", PROXY, REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD, REDDIT_USER_AGENT])
except Exception as e:
    print(e)
