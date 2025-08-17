from sheet import GoogleSheetsAPI
from dotenv import load_dotenv, find_dotenv

loaded = load_dotenv(find_dotenv())  

my_sheet = GoogleSheetsAPI()
my_sheet.verify_sheet()
channel_url = my_sheet.get_channel_url(2)
print(f"Channel URL: {channel_url}")