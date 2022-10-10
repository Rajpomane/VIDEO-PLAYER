import os
import signal
import sys
import re
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pytgcalls import idle as pyidle
from pytgcalls import PyTgCalls
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityAudio
from pytgcalls.types.input_stream.quality import HighQualityVideo, MediumQualityVideo, LowQualityVideo
from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch
from time import time
from dotenv import load_dotenv
from datetime import datetime
import dotenv


async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)

# VPS 
if os.path.exists(".env"):
    load_dotenv(".env")

# YTDL
# https://github.com/pytgcalls/pytgcalls/blob/dev/example/youtube_dl/youtube_dl_example.py
async def get_youtube_stream(ytlink):
        proc = await asyncio.create_subprocess_exec(
            'youtube-dl',
            '-g',
            '-f',
            # CHANGE THIS BASED ON WHAT YOU WANT
            'best[height<=?720][width<=?1280]',
            f'{ytlink}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        return stdout.decode().split('\n')[0]



# Client and PyTgCalls
API_ID = int(os.getenv("API_ID", "6"))
API_HASH = os.getenv("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
SESSION = os.getenv("SESSION")
CHAT = int(os.getenv("CHAT", "6"))
HNDLR = os.getenv("HNDLR", "!")

bot = Client(SESSION, API_ID, API_HASH)
call_py = PyTgCalls(bot)
GROUP_CALL = []


@bot.on_message(filters.me & filters.command("vstream", prefixes=f"{HNDLR}"))
async def stream(client, m: Message):
   if len(m.command) < 2:
      await m.reply("`Give A Link/LiveLink/.m3u8 URL/YTLink to Stream from 🎶`")
   else:
      if len(m.command)==2:
         link = m.text.split(None, 1)[1]
         q = HighQualityVideo()
         huehue = await m.reply("`Trying to Stream 💭`")
      elif len(m.command)==3:
         op = m.text.split(None, 1)[1]
         link = op.split(None, 1)[0]
         quality = op.split(None, 1)[1]
         if quality=="720":
            q = HighQualityVideo()
         elif quality=="480":
            q = MediumQualityVideo()
         elif quality=="360":
            q = LowQualityVideo()
         else:
            q = HighQualityVideo()
            await m.reply("`Use 360/480/720`")
         huehue = await m.reply("`Trying to Stream 💭`")
      else:
         await m.reply("`!vstream {link} {720/480/360}`")
      chat_id = m.chat.id

      # Filtering out YouTube URL's
      regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
      match = re.match(regex,link)
      if match:
         try:
            livelink = await get_youtube_stream(link)
         except Exception as e:
            await huehue.edit(f"**YTDL ERROR** \n{e}")
      else:
         livelink = link
      print(livelink)

      # Playing
      if chat_id in GROUP_CALL:
         try:
            await call_py.leave_group_call(chat_id)
            await asyncio.sleep(2)
            await call_py.join_group_call(
               chat_id,
               AudioVideoPiped(
                  livelink,
                  HighQualityAudio(),
                  q
               ),
               stream_type=StreamType().pulse_stream,
            )
            await huehue.delete()
            await m.reply(f"Started [Streaming]({livelink}) in `{chat_id}`", disable_web_page_preview=True)
         except Exception as ep:
            await m.reply(f"{ep}")
      else:
         try:
            await call_py.join_group_call(
               chat_id,
               AudioVideoPiped(
                  livelink,
                  HighQualityAudio(),
                  q
               ),
               stream_type=StreamType().pulse_stream,
            )
            GROUP_CALL.append(chat_id)
            await huehue.delete()
            await m.reply(f"Started [Streaming]({livelink}) in `{chat_id}`", disable_web_page_preview=True)
         except Exception as ep:
            await m.reply(f"{ep}")

@bot.on_message(filters.me & filters.command("vplay", prefixes=f"{HNDLR}"))
async def play(client, m: Message):
   replied = m.reply_to_message
   chat_id = m.chat.id
   if replied:
      if replied.document or replied.video:
         huehue = await replied.reply("`Downloading 📩`")
         location = await replied.download()
         if len(m.command) < 2:
            q = HighQualityVideo()
         else:
            pq = m.text.split(None, 1)[1]
            if pq=="720":
               q = HighQualityVideo()
            elif pq=="480":
               q = MediumQualityVideo()
            elif pq=="360":
               q = LowQualityVideo()
            else:
               q = HighQualityVideo()
               await huehue.edit("`Only 720, 480, 360 Allowed` \n`Now Streaming in 720p`")
         if chat_id in GROUP_CALL:
            try:
               await call_py.leave_group_call(chat_id)
               await asyncio.sleep(2)
               await call_py.join_group_call(
                  chat_id,
                  AudioVideoPiped(
                     location,
                     HighQualityAudio(),
                     q
                  ),
                  stream_type=StreamType().local_stream,
               )
               await huehue.delete()
               await replied.reply(f"Started Playing in `{chat_id}`", disable_web_page_preview=True)
            except Exception as ep:
               await m.reply(f"{ep}")
         else:
            try:
               await call_py.join_group_call(
                  chat_id,
                  AudioVideoPiped(
                     location,
                     HighQualityAudio(),
                     q
                  ),
                  stream_type=StreamType().local_stream,
               )
               GROUP_CALL.append(chat_id)
               await huehue.delete()
               await replied.reply(f"Started Playing in `{chat_id}`", disable_web_page_preview=True)
            except Exception as ep:
               await m.reply(f"{ep}")
      else:
         if len(m.command) < 2:
            await replied.reply("`Either Reply to a VIDEO or Give me Query/YT Link to Play`")
         else:
            try:
               query = m.text.split(None, 1)[1]
               hmmop = await m.reply("`Searching 🔎`")
               search = VideosSearch(query, limit=1)
               for result in search.result()["result"]:
                  ytid = result['id']
                  url = f"https://www.youtube.com/watch?v={ytid}"
            except Exception as ey:
               print(ey)
               await m.reply("`Found Nothing :( Try searching something Else.`")
            ytlink = await get_youtube_stream(url)
            print(ytlink)
            # Playing
            if chat_id in GROUP_CALL:
               try:
                  await call_py.leave_group_call(chat_id)
                  await asyncio.sleep(2)
                  await call_py.join_group_call(
                     chat_id,
                     AudioVideoPiped(
                        ytlink,
                        HighQualityAudio(),
                        MediumQualityVideo()
                     ),
                     stream_type=StreamType().pulse_stream,
                  )
                  await hmmop.delete()
                  await m.reply(f"Started [Streaming]({ytlink}) in `{chat_id}`", disable_web_page_preview=True)
               except Exception as ep:
                  await m.reply(f"{ep}")
            else:
               try:
                  await call_py.join_group_call(
                     chat_id,
                     AudioVideoPiped(
                        ytlink,
                        HighQualityAudio(),
                        MediumQualityVideo()
                     ),
                     stream_type=StreamType().pulse_stream,
                  )
                  GROUP_CALL.append(chat_id)
                  await hmmop.delete()
                  await m.reply(f"Started [Streaming]({livelink}) in `{chat_id}`", disable_web_page_preview=True)
               except Exception as ep:
                  await m.reply(f"{ep}")
   
   else:
         if len(m.command) < 2:
            await replied.reply("`Either Reply to a VIDEO or Give me Query/YT Link to Play`")
         else:
            try:
               query = m.text.split(None, 1)[1]
               hmmop = await m.reply("`Searching 🔎`")
               search = VideosSearch(query, limit=1)
               for result in search.result()["result"]:
                  ytid = result['id']
                  url = f"https://www.youtube.com/watch?v={ytid}"
            except Exception as ey:
               print(ey)
               await m.reply("`Found Nothing :( Try searching something Else.`")
            ytlink = await get_youtube_stream(url)
            print(ytlink)
            # Playing
            if chat_id in GROUP_CALL:
               try:
                  await call_py.leave_group_call(chat_id)
                  await asyncio.sleep(2)
                  await call_py.join_group_call(
                     chat_id,
                     AudioVideoPiped(
                        ytlink,
                        HighQualityAudio(),
                        MediumQualityVideo()
                     ),
                     stream_type=StreamType().pulse_stream,
                  )
                  await hmmop.delete()
                  await m.reply(f"Started [Streaming]({ytlink}) in `{chat_id}`", disable_web_page_preview=True)
               except Exception as ep:
                  await m.reply(f"{ep}")
            else:
               try:
                  await call_py.join_group_call(
                     chat_id,
                     AudioVideoPiped(
                        ytlink,
                        HighQualityAudio(),
                        MediumQualityVideo()
                     ),
                     stream_type=StreamType().pulse_stream,
                  )
                  GROUP_CALL.append(chat_id)
                  await hmmop.delete()
                  await m.reply(f"Started [Streaming]({ytlink}) in `{chat_id}`", disable_web_page_preview=True)
               except Exception as ep:
                  await m.reply(f"{ep}")

@bot.on_message(filters.me & filters.command("pause", prefixes=f"{HNDLR}"))
async def pause(client, m: Message):
   chat_id = m.chat.id
   await call_py.pause_stream(chat_id)
   await m.reply("`Paused Streaming ⏸️`")

@bot.on_message(filters.me & filters.command("resume", prefixes=f"{HNDLR}"))
async def resume(client, m: Message):
   chat_id = m.chat.id
   await call_py.resume_stream(chat_id)
   await m.reply("`Resumed Streaming ▶`") 

@bot.on_message(filters.me & filters.command("vstop", prefixes=f"{HNDLR}"))
async def stop(client, m: Message):
   try:
      chat_id = m.chat.id
      if chat_id in GROUP_CALL:
         GROUP_CALL.remove(chat_id)
      else:
         pass
      await call_py.leave_group_call(chat_id)
      await m.reply("`Stopped Streaming ⏹️`")
   except Exception as e:
      print(e)






call_py.start()
pyidle()

