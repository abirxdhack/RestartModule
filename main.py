# main.py
from pyrogram import Client
from restart import setup_restart_handler

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Set up the restart handler
setup_restart_handler(app)

app.run()
