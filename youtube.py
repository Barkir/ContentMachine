import os
from dotenv import load_dotenv
from googleapiclient.discovery import build 
import re

load_dotenv()


class YouTubeAPI:
    def __init__(self):
        self.credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE')
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.yt = build(
            'youtube', 'v3',
            developerKey=self.api_key)
    
    def get_channel_info(self, channel_id):
        channel_id = self.parse_channel_input(channel_id)
        print(channel_id)
        try:
            res = self.yt.search().list(
                part='snippet',
                type='channel',
                q=channel_id
            ).execute()
            items = res.get('items', [])
            if not items:
                print(f"No channel found for ID: {channel_id}")
                return None
            print(f"Channel found: {items[0]['snippet']['title']}")
            return items[0]['snippet']
        except Exception as e:
            print(f"Error {e}")
    
    def parse_channel_input(self, s: str):
        splitted = s.split('/')
        if len(splitted) > 1 and splitted[-1].startswith('@'):
            return splitted[-1]
        print(f"Invalid channel ID format: {s}")
        return None
        