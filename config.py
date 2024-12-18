import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMIN_LIST = os.getenv("ADMIN_LIST")
FUSION_BRAIN_API_KEY = os.getenv("FUSION_BRAIN_API_KEY")
FUSION_BRAIN_SECRET_KEY = os.getenv("FUSION_BRAIN_SECRET_KEY")
QUOTES_API_KEY=os.getenv("QUOTES_API_KEY")