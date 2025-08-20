from sheet import GoogleSheetsAPI
from dotenv import load_dotenv, find_dotenv
from constants import *
from pprint import pprint

loaded = load_dotenv(find_dotenv())  


# What will this program do?
# 1. Cycling through channels from the table
# 2. Getting info about them
# Then we create other sheet named by this channel and add info about a channel there.

youtube_sheet = GoogleSheetsAPI(sheet_name=YOUTUBE_SHEET_NAME)
num_rows = 10

for i in range(START_FROM, num_rows+START_FROM):
    youtube_sheet.create_new_sheet(youtube_sheet.get_channel_name(i))
    info = youtube_sheet.get_channel_info(i, videos=10)
    youtube_sheet.append_rows(info)