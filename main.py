from sheet import GoogleSheetsAPI
from dotenv import load_dotenv, find_dotenv
from constants import *

loaded = load_dotenv(find_dotenv())  

youtube_sheet = GoogleSheetsAPI(sheet_name=YOUTUBE_SHEET_NAME)
youtube_sheet.get_channel_info(3)
# instagram_sheet = GoogleSheetsAPI(sheet_name=INSTAGRAM_SHEET_NAME)
# tiktok_sheet = GoogleSheetsAPI(sheet_name=TIKTOK_SHEET_NAME)
# twitter_sheet = GoogleSheetsAPI(sheet_name=TWITTER_SHEET_NAME)