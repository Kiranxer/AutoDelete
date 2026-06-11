import threading

from pyrogram import Client

from config import API_ID
from config import API_HASH
from config import BOT_TOKEN

from web import app as web_app

from handlers.start import register_start

def run_web():
    web_app.run(
        host="0.0.0.0",
        port=8000
    )

bot = Client(
    "AutoDeleteBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

register_start(bot)

if __name__ == "__main__":

    threading.Thread(
        target=run_web,
        daemon=True
    ).start()

    bot.run()
