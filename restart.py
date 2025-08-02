import os
import shutil
import asyncio
import subprocess
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID, UPDATE_CHANNEL_URL, COMMAND_PREFIX
from core import auth_admins, restart_messages
from utils import LOGGER

async def get_auth_admins():
    try:
        admins = await auth_admins.find({}, {"user_id": 1, "_id": 0}).to_list(None)
        return {admin["user_id"] for admin in admins}
    except Exception as e:
        LOGGER.error(f"Failed to fetch authorized admins: {e}")
        return set()

async def is_admin(user_id):
    if user_id == OWNER_ID:
        return True
    auth_admin_ids = await get_auth_admins()
    return user_id in auth_admin_ids

def check_session_permissions(session_file: str) -> bool:
    if not os.path.exists(session_file):
        LOGGER.warning(f"Session file {session_file} not found")
        return True
    if not os.access(session_file, os.W_OK):
        LOGGER.error(f"Session file {session_file} is not writable")
        try:
            os.chmod(session_file, 0o600)
            LOGGER.info(f"Set write permissions for {session_file}")
            return os.access(session_file, os.W_OK)
        except Exception as e:
            LOGGER.error(f"Failed to set permissions for {session_file}: {e}")
            return False
    return True

def setup_restart_handler(app: Client):
    @app.on_message(filters.command(["restart", "reboot", "reload"], prefixes=COMMAND_PREFIX) & (filters.private | filters.group))
    async def restart(client: Client, message):
        user_id = message.from_user.id
        if not await is_admin(user_id):
            return
        LOGGER.info(f"Restart command received from user {user_id}")
        response = await client.send_message(
            chat_id=message.chat.id,
            text="**Restarting bot... Please wait.**",
            parse_mode=ParseMode.MARKDOWN
        )
        session_file = "SmartTools.session"
        if not check_session_permissions(session_file):
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=response.id,
                text="**Failed To Restart Due To ReadOnly Environment**",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        directories = ["downloads", "temp", "temp_media", "data", "repos", "temp_dir"]
        for directory in directories:
            try:
                if os.path.exists(directory):
                    shutil.rmtree(directory)
                    LOGGER.info(f"Cleared directory: {directory}")
            except Exception as e:
                LOGGER.error(f"Failed to clear directory {directory}: {e}")
        log_file = "botlog.txt"
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
                LOGGER.info(f"Cleared log file: {log_file}")
            except Exception as e:
                LOGGER.error(f"Failed to clear log file {log_file}: {e}")
        start_script = "start.sh"
        if not os.path.exists(start_script):
            LOGGER.error("Start script not found")
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=response.id,
                text="**Failed To Restart Due To Unix Issue❌**",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        try:
            await restart_messages.insert_one({
                "chat_id": message.chat.id,
                "msg_id": response.id
            })
            LOGGER.info(f"Stored restart message details for chat {message.chat.id}")
            subprocess.Popen(["bash", start_script])
            os._exit(0)
        except Exception as e:
            LOGGER.error(f"Restart command execution failed: {e}")
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=response.id,
                text="**Failed To Restart Invalid LF Format❌**",
                parse_mode=ParseMode.MARKDOWN
            )

    @app.on_message(filters.command(["stop", "kill", "off"], prefixes=COMMAND_PREFIX) & (filters.private | filters.group))
    async def stop(client: Client, message):
        user_id = message.from_user.id
        if not await is_admin(user_id):
            return
        LOGGER.info(f"Stop command received from user {user_id}")
        response = await client.send_message(
            chat_id=message.chat.id,
            text="**Stopping bot and clearing data...**",
            parse_mode=ParseMode.MARKDOWN
        )
        directories = ["downloads", "temp", "temp_media", "data", "repos"]
        for directory in directories:
            try:
                if os.path.exists(directory):
                    shutil.rmtree(directory)
                    LOGGER.info(f"Cleared directory: {directory}")
            except Exception as e:
                LOGGER.error(f"Failed to clear directory {directory}: {e}")
        log_file = "botlog.txt"
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
                LOGGER.info(f"Cleared log file: {log_file}")
            except Exception as e:
                LOGGER.error(f"Failed to clear log file {log_file}: {e}")
        try:
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=response.id,
                text="**Bot stopped successfully, data cleared**",
                parse_mode=ParseMode.MARKDOWN
            )
            os._exit(0)
        except Exception as e:
            LOGGER.error(f"Failed to stop bot: {e}")
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=response.id,
                text="**Failed To Stop Bot Due To Telegram Limit ❌ **",
                parse_mode=ParseMode.MARKDOWN
            )
