from pyrogram.enums import ParseMode 
from utils import LOGGER
from core import setup_restart_handlers, restart_messages
from app import app
from user import user
import asyncio

async def main():
    await app.start()
    await user.start()
    LOGGER.info("Bot Successfully Started! 💥")
    try:
        restart_data = await restart_messages.find_one()
        if restart_data:
            try:
                await app.edit_message_text(
                    chat_id=restart_data["chat_id"],
                    message_id=restart_data["msg_id"],
                    text="**Restarted Successfully 💥**",
                    parse_mode=ParseMode.MARKDOWN
                )
                await restart_messages.delete_one({"_id": restart_data["_id"]})
                LOGGER.info(f"Restart message updated and cleared from database for chat {restart_data['chat_id']}")
            except Exception as e:
                LOGGER.error(f"Failed to update restart message: {e}")
    except Exception as e:
        LOGGER.error(f"Failed to fetch restart message from database: {e}")
    setup_restart_handlers(app)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_forever()
    except KeyboardInterrupt:
        LOGGER.info("Bot Stopped Successfully!")
        try:
            if loop.is_running():
                loop.run_until_complete(asyncio.gather(app.stop(), user.stop()))
            else:
                asyncio.run(asyncio.gather(app.stop(), user.stop()))
        except Exception as e:
            LOGGER.error(f"Failed to stop clients: {e}")
        finally:
            if not loop.is_closed():
                loop.close()
