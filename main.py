import os
import signal
import sys
import re
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from config import config, app
from dotenv import load_dotenv
from datetime import datetime
import dotenv


import asyncio
import time

from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pyrogram import Client




mongo = MongoClient(config.MONGO_DB_URI)
db = mongo.AFK


cleanmode = {}






app.start()
idle()



