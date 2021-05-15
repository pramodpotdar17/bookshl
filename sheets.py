import gspread
from oauth2client.service_account import ServiceAccountCredentials
from random import randint
import datetime

def get_random_highlight():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)

    # real code starts
    highlights = client.open('highlights').sheet1
    highlightsPosted = client.open('highlightsPosted').sheet1

    count = len(highlights.get_all_records()) + 1

    rownum = randint(1, count)
    row = highlights.row_values(rownum)
    # print(rownum, row)

    highlights.delete_rows(rownum)

    now = str(datetime.datetime.now())
    highlightsPosted.append_rows([row+[now]])
    return row
