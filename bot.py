import threading
import asyncio

from pyrogram import Client

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN
)

from web import app as web_app

from handlers.start import register_start

from utils.scheduler import (
    set_bot,
    start_scheduler,
    restore_jobs
)


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


# Register handlers
register_start(bot)

# More handlers will be added later
# register_settings(bot)
# register_messages(bot)


async def startup():

    set_bot(bot)

    start_scheduler()

    await restore_jobs()

    print("✅ Scheduler started")
    print("✅ Jobs restored")


if __name__ == "__main__":

    # Start Koyeb health web server
    threading.Thread(
        target=run_web,
        daemon=True
    ).start()

    # Start bot
    bot.start()

    # Run startup tasks
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        startup()
    )

    print("🤖 Auto Delete Bot Started")

    # Keep running
    asyncio.get_event_loop().run_forever()
