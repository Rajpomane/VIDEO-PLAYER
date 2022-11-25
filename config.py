import os
import signal
import sys
import re
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message

from dotenv import load_dotenv
import dotenv
import os
import asyncio
import time

from dotenv import load_dotenv
from pyrogram import Client, filters


# Necessary Vars
async def _human_time_duration(seconds):
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
HNDLR = os.getenv("HNDLR", ".")

app = Client(SESSION, API_ID, API_HASH, plugins=dict(root="Modules"))






