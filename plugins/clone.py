import re
import logging
from pymongo import MongoClient

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors.exceptions.bad_request_400 import AccessTokenExpired, AccessTokenInvalid
from info import DB_URI as MONGO_URL

mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["cloned_vgbotz"]

async def start_bot(bot_token, api_id, api_hash, clone_text):
    try:
        ai = Client(
            f"{bot_token}", api_id, api_hash,
            bot_token=bot_token,
            plugins={"root": "clone_plugins"},
        )
        
        await ai.start()
        bot = await ai.get_me()
        details = {
            'bot_id': bot.id,
            'is_bot': True,
            'name': bot.first_name,
            'token': bot_token,
            'username': bot.username
        }
        mongo_db.bots.insert_one(details)
        return f"<b>sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʟᴏɴᴇᴅ ʏᴏᴜʀ ʙᴏᴛ: @{bot.username}.\n\nʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ sᴇᴛ ʏᴏᴜʀ sʜᴏʀᴛɴᴇʀ ɪɴ ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏ sᴛᴀʀᴛ ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ</b>"
    except BaseException as e:
        logging.exception("Error while cloning bot.")
        return f"⚠️ <b>Bot Error:</b>\n\n<code>{e}</code>\n\nKindly forward this message to @tanjiro_x_coder to get assistance."

@Client.on_message(filters.command("clone") & filters.private)
async def clone(client, message):
    await message.reply_text("Specify bot parameters to clone.")

@Client.on_message((filters.regex(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}')) & filters.private)
async def on_clone(client, message):
    try:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        bot_token = re.findall(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}', message.text, re.IGNORECASE)
        bot_token = bot_token[0] if bot_token else None
        bot_id = re.findall(r'\d[0-9]{8,10}', message.text)
        bots = list(mongo_db.bots.find())
        bot_tokens = None  # Initialize bot_tokens variable

        for bot in bots:
            bot_tokens = bot['token']

        forward_from_id = message.forward_from.id if message.forward_from else None
        if bot_tokens == bot_token and forward_from_id == 93372553:
            await message.reply_text("©️ ᴛʜɪs ʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴄʟᴏɴᴇᴅ ʙᴀʙʏ 🐥")
            return

        if not forward_from_id != 93372553:
            msg = await message.reply_text("👨‍💻 ᴡᴀɪᴛ ᴀ ᴍɪɴᴜᴛᴇ ɪ ᴀᴍ ᴄʀᴇᴀᴛɪɴɢ ʏᴏᴜʀ ʙᴏᴛ ❣️")
            result = await start_bot(bot_token, API_ID, API_HASH, script.CLONE_TXT)
            await msg.edit_text(result)
    except Exception as e:
        logging.exception("Error while handling message.")
      
