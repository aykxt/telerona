import logging
import os
import sys

from dotenv import load_dotenv
from telethon import TelegramClient

from . import utils
from .database import Database

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

load_dotenv()
try:
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")
except KeyError:
    logger.error("One or more environment variables are missing! Exiting now…")
    sys.exit(1)


db = Database(DATABASE_URL)

loc_btn = utils.create_loc_buttons()

bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

from .api_helper import Api

api = Api()
