import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")          # Токен от @BotFather
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")  # Ключ с console.anthropic.com
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@instruktionforlife")
