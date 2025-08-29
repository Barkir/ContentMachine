YOUTUBE_SHEET_NAME="youtube"
INSTAGRAM_SHEET_NAME="instagram"
TIKTOK_SHEET_NAME="tiktok"
TWITTER_SHEET_NAME="twitter"
DOWNLOADS_PATH="/home/kirill/Side-Projects/ContentMachine/downloads/"
AUDIOS_PATH=DOWNLOADS_PATH+"audios/"
VIDEOS_PATH=DOWNLOADS_PATH+"videos/"
TRANSCRIBED_PATH="openai_data/"
START_FROM = 2

POST_PROMPT="Создай детальный пост в телеграме по этому тексту. Используй меньше стикеров и эмодзи." \
"Не делай этот пост слишком веселым и вдохновляющим. Нужно передать более стоическое отношение к этому всему. " \
"В конце задай интересный вопрос аудитории."

IMAGE_PROMPT="Сгенерируй промпт для генерации изображения из этого текста. Изображение должно быть в художественном стиле. " \
                "Картина должна быть нарисована масляными красками."