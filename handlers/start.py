from pyrogram import filters
from pyrogram.types import Message

def register_start(app):

    @app.on_message(filters.private & filters.command("start"))
    async def start_handler(client, message: Message):

        await message.reply_text(
            "👋 Welcome to Auto Delete Bot\n\n"
            "Add me to a group and promote me as admin."
        )
