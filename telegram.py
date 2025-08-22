# Brief plan
# 1. This is a bot whom is sent a message (link to a video or to a post or some prompt for a post)
# 2. He converts it to a telegram post with a picture and posts it to a channel.

# Transcribing module mustn't be located here! We must call a transcribing api if we see a link to a video.
# Here's a brief pipeline.

# Sending message ->
# if it is a link then
#   call transcribing module
#   call a function to turn transcribition into a post
#   send it to the user and get the approve
#   post it
# if it is an idea for a post then
#   call a function to turn idea to post
#   send it to the user and get the approve
#   post it5е
from dotenv import load_dotenv
import os

load_dotenv()

def data_is_link(data):
    pass

class TelegramAssistant:
    def __init__(self):
        self.openai_audio_api = os.getenv("OPENAI_AUDIO_KEY")
        self.bot_token = os.getenv("TG_BOT_TOKEN")

    def transcribe_from_link(self, link):
        # video = download_video_by_link(ling)
        # audio = get_audio_from_video(video)
        # text = some_command_from_openai(audio)
        # return text
        
        pass

    def text_to_post(self, text):
        pass

    def get_data(self, data):
        result = self.transcribe_msg(data) if data_is_link(data) else self.text_to_post(data)
        # printResulttotgChannel(result)
            