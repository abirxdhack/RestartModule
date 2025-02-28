from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import os
import sys
from config import ADMIN_IDS

def setup_restart_handler(app: Client):
    @app.on_message(filters.command(["restart"], prefixes=["/", "."]) & filters.private)
    async def restart_bot(client, message):
        if message.from_user.id not in ADMIN_IDS:
            await message.reply_text(
                "<b>❌ You are not authorized to use this command.</b>", 
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("👨🏼‍💻 Developer", url='https://t.me/abirxdhackz'),
                            InlineKeyboardButton("🤖 Other Bots", url="https://t.me/Modvip_rm")    
                        ],
                        [
                            InlineKeyboardButton("🔗 Source Code", url="https://github.com/abirxdhack"),
                            InlineKeyboardButton("⚙️ Update Channel", url="https://t.me/Modvip_rm")
                        ]
                    ]
                )
            )
            return

        msg = await message.reply_text("<b>🔄 Restarting the bot...</b>", parse_mode=ParseMode.HTML)
        await asyncio.sleep(2)
        await msg.edit_text("<b> Bot Successfully Started! 💥</b>", parse_mode=ParseMode.HTML)
        
        os.execl(sys.executable, sys.executable, *sys.argv)