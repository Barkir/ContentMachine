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
import requests
import json
import os
import re
import base64
import uuid

from langchain_openai import ChatOpenAI
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

# =============================
# Transribing and post creation
# =============================

    # save param for saving audio file locally or not
    def transcribe_from_link(self, link):
        audio_name = self.yt_client.download_audio(link)

        llm = ChatOpenAI(base_url="https://openrouter.ai/api/v1",
            model="gpt-4o-audio-preview",
            temperature=0,
            max_completion_tokens=None,
            timeout=None,
            max_retries=2
        )
        with open(audio_name, "rb") as f:
            audio_data = f.read()
            audio_b64 = base64.b64encode(audio_data).decode()

            messages = [
                    (
                        "human",
                        [
                            {"type": "text", "text": "Transcribe the following"},
                            {"type": "input_audio", "input_audio": {"data": audio_b64, "format": "mp3"}},
                        ],
                    )
            ]
        
        output = llm.invoke(messages)
        return output.content

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

    def text_to_image(self, text, prompt=IMAGE_PROMPT):
        image_prompt = self.text_to_post(text, prompt=prompt)
        
        prompt = f"{image_prompt}\n\n{text}"
        completion = self.openai_client.chat.completions.create(
            model="google/gemini-2.5-flash-image-preview:free",
            messages=[
                {"role": "user", "content": "You are helpful assistant that creates engaging images"},
                {"role": "user", "content": image_prompt}
            ]
        )
        print(completion.choices[0].images.url)






    def get_data(self, data, path=TRANSCRIBED_PATH):
        if data_is_link(data):
            print("It's a link!")
            text = self.transcribe_from_link(data)
            filename = f"{path}{uuid.uuid4()}.txt"
            with open(filename, "w") as f:
                f.write(data + "\n" + text)
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

            