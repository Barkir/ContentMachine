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
from openai import OpenAI
from youtube import YouTubeAPI
from constants import *
import os
import re

from telegram import InputFile
from telegram.constants import ParseMode
from telegram.ext import Application, AIORateLimiter

load_dotenv()

def data_is_link(data: str) -> bool:
    url_pattern = r'^https?://'
    return re.match(url_pattern, data) is not None

class TelegramAssistant:
    def __init__(self):
        self.openai_audio_api = os.getenv("OPENAI_API_KEY")
        self.bot_token = os.getenv("TG_BOT_TOKEN")
        self.channel_id = os.getenv("TG_CHANNEL_ID")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # --- OpenAI / Youtube ---
        self.openai_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=self.openai_api_key)
        self.yt_client = YouTubeAPI()

        # --- PTB Application (async) ---
        self.app = Application.builder().token(self.bot_token).rate_limiter(AIORateLimiter()).build()

    # save param for saving audio file locally or not
    def transcribe_from_link(self, link, save=True):
        audio_name = self.yt_client.download_audio(link)
        with open(audio_name, "rb") as f:
            transcript = self.openai_client.chat.completions.create(
                model="openai/gpt-4o-audio-preview",
                messages=[
                    {"role": "user", "content": "Please transcribe the following audio."}
                ],
                audio={"file": f, "mimetype": "audio/mpeg"})
        
        text = transcript.choices[0].message.content.strip()
        if save:
            txt_name = audio_name.rsplit(".", 1)[0] + ".txt"
            with open(txt_name, "w", encoding="utf-8") as txt_file:
                txt_file.write(text)
        
        return text

    def text_to_post(self, text, prompt=POST_PROMPT):
        prompt = f"{prompt}\n\n{text}"
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates engaging telegram posts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        post = response.choices[0].message.content.strip()
        return post

    def get_data(self, data):
        if data_is_link(data):
            print("It's a link!")
            text = self.transcribe_from_link(data)
            return self.text_to_post(text)
        else:
            return self.text_to_post(data)
    
    def _split_text(self, text, max_length=4096):
        paragraphs = text.split('\n')
        chunks = []
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) + 1 <= max_length:
                current_chunk += para + '\n'
            else:
                chunks.append(current_chunk.strip())
                current_chunk = para + '\n'

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    async def send_post(self, post_text, parse_mode=ParseMode.MARKDOWN, disable_preview=False):
        chunks = self._split_text(post_text)
        for chunk in chunks:
            await self.app.bot.send_message(
                chat_id=self.channel_id,
                text=chunk,
                parse_mode=parse_mode
            )

    async def send_image(self, image_path, caption=None, parse_mode=ParseMode.MARKDOWN):
        if re.match(r'^https?://', image_path):
            await self.app.bot.send_photo(
                chat_id=self.channel_id,
                photo=image_path,
                caption=caption,
                parse_mode=parse_mode
            )
        else:
            with open(image_path, 'rb') as img_file:
                await self.app.bot.send_photo(
                    chat_id=self.channel_id,
                    photo=InputFile(img_file),
                    caption=caption,
                    parse_mode=parse_mode
                )
    async def post_to_channel(self, data, image_path=None):
        post_text = self.get_data(data)
        if image_path:
            await self.send_image(image_path, caption=post_text)
        else:
            await self.send_post(post_text)
    
    def run_polling(self):
        self.app.run_polling()

            