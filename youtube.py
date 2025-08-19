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
                channelId=channel_id
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
        s = s.strip()
        # UC… (готовый channelId)
        if re.fullmatch(r"UC[\w-]{22}", s):
            return {"channel_id": s}

        # URL вида /channel/UC..., /@handle, /user/..., /c/...
        if "youtube.com" in s:
            # /channel/UC...
            m = re.search(r"/channel/(UC[\w-]{22})", s)
            if m:
                return {"channel_id": m.group(1)}
            # /@handle
            m = re.search(r"youtube\.com/@([A-Za-z0-9_.-]+)", s)
            if m:
                return {"handle": m.group(1)}
            # кастомные /c/... или /user/... — оставим как поисковый запрос
            return {"query": s}

        # @handle
        if s.startswith("@"):
            return {"handle": s[1:]}

        # Иначе — это произвольное имя, поиск
        return {"query": s}