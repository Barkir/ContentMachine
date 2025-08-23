from sheet import GoogleSheetsAPI
from dotenv import load_dotenv, find_dotenv
from constants import *
from pprint import pprint
from youtube import YouTubeAPI
from telegram_bot import TelegramAssistant
import asyncio

loaded = load_dotenv(find_dotenv())  


# What will this program do?
# 1. Cycling through channels from the table
# 2. Getting info about them
# Then we create other sheet named by this channel and add info about a channel there.

youtube_sheet = GoogleSheetsAPI(sheet_name=YOUTUBE_SHEET_NAME)
telegram_bot = TelegramAssistant()
link = "https://www.youtube.com/shorts/1-IYAbvqjTM"
post_text = telegram_bot.get_data(link)
asyncio.run(telegram_bot.send_post(post_text))

# num_rows = 10
# youtubeObj = YouTubeAPI()
# youtubeObj.download_video("https://www.youtube.com/watch?v=eJHDIQaHZfs")
# youtubeObj.download_audio("https://www.youtube.com/watch?v=eJHDIQaHZfs")

# for i in range(START_FROM, num_rows+START_FROM):
#     youtube_sheet.create_new_sheet(youtube_sheet.get_channel_name(i))
#     info = youtube_sheet.get_channel_info(i, videos=10)
#     youtube_sheet.append_rows(info)