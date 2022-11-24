import os
import signal
import sys
import re
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message

from dotenv import load_dotenv
from datetime import datetime
import dotenv


async def _human_time_duration(seconds):
MONGO_DB_URI = getenv("MONGO_DB_URI", None)  
API_ID = int(os.getenv("API_ID", "6"))
API_HASH = os.getenv("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
SESSION = os.getenv("SESSION")
HNDLR = os.getenv("HNDLR", ".")
