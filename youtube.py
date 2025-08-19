import os
from dotenv import load_dotenv
from googleapiclient.discovery import build 
import re
from pprint import pprint

load_dotenv()


class YouTubeAPI:
    def __init__(self):
        self.credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE')
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.yt = build(
            'youtube', 'v3',
            developerKey=self.api_key)
    
    def get_channel_info(self, channel_id, videos=10):
        channel_id = self.parse_channel_input(channel_id)
        print(channel_id)
        try:
            res = self.yt.search().list(
                part='snippet',
                type='channel',
                q=channel_id
            ).execute()
            if not res.get('items'):
                print("No channel found with the provided ID.")
                return None
            
            uploads = self.get_uploads_list(res)
            if uploads:
                videos_list = self.fetch_n_videos(uploads, videos)
                return videos_list
            else:                
                print("No uploads playlist found for the channel.")
                return None
    
        except Exception as e:
            print(f"Error {e}")
    
    def fetch_n_videos(self, uploads, count):
        out = []
        print(uploads)
        while (len(out) < count):
            pl = self.yt.playlistItems().list(
                part='contentDetails',
                playlistId=uploads,
                maxResults=count - len(out),
                pageToken=None
            ).execute()

            ids = [x["contentDetails"]["videoId"] for x in pl.get("items", [])]
            if not ids:
                print("No videos found in the playlist.")
                break
            vres = self.yt.videos().list(
                part='snippet,statistics',
                id=','.join(ids)
            ).execute() 

            for v in vres.get('items', []):
                out.append({
                    "id": v["id"],
                    "title": v["snippet"]["title"],
                    "views": v["statistics"].get("viewCount", 0),
                    "likes": v["statistics"].get("likeCount", 0),
                    "comments": v["statistics"].get("commentCount", 0),
                    "url": f"https://www.youtube.com/watch?v={v['id']}"
                })

                if len(out) >= count:
                    break
            token = pl.get('nextPageToken')
            if not token:
                print("No more pages to fetch.")
                break
        return out
    
    def get_uploads_list(self, found_channel):
        items = found_channel.get('items', [])
        if not items:
            print("No items found for the channel.")
            return None
        print(f"Items found: {len(items)}")
        # pprint(items)
        found_channel_id = items[0].get('id')["channelId"]
        res = self.yt.channels().list(
            part='snippet,contentDetails,statistics',
            id=found_channel_id
        ).execute()
        if not res.get('items'):
            print("No channel details found.")
            return None
        
        return res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    
    def parse_channel_input(self, s: str):
        splitted = s.split('/')
        if len(splitted) > 1 and splitted[-1].startswith('@'):
            return splitted[-1]
        print(f"Invalid channel ID format: {s}")
        return None
        