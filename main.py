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
app = Client(SESSION, API_ID, API_HASH, plugins=dict(root="Modules"))

import asyncio
import time

from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pyrogram import Client

import config

loop = asyncio.get_event_loop()
boot = time.time()

mongo = MongoClient(config.MONGO_DB_URI)
db = mongo.AFK

appid = 0
appame = ""
appusername = ""

cleanmode = {}


getme = await app.get_me()
appid = getme.id
appusername = (getme.username).lower()
if getme.last_name:
  appname = getme.first_name + " " + getme.last_name
else:
  appname = getme.first_name




app.start()
idle()



