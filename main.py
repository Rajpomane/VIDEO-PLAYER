import os
import signal
import sys
import re
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from config import config
from dotenv import load_dotenv
from datetime import datetime
import dotenv


async def _human_time_duration(seconds): 
API_ID = int(os.getenv("API_ID", "6"))
API_HASH = os.getenv("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
SESSION = os.getenv("SESSION")
HNDLR = os.getenv("HNDLR", ".")
app = Client(SESSION, API_ID, API_HASH, plugins=dict(root="Modules"))

import asyncio
import time

from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pyrogram import Client




mongo = MongoClient(config.MONGO_DB_URI)
db = mongo.AFK


cleanmode = {}






app.start()
idle()



