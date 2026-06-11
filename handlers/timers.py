from pyrogram import filters
from pyrogram.types import Message

from database.settings import (
    set_timer,
    get_status_text
)


VALID_TYPES = [
    "text",
    "photo",
    "video",
    "document",
    "sticker",
    "animation",
    "voice",
    "audio"
]


async def is_admin(
    client,
    chat_id,
    user_id
):

    member = await client.get_chat_member(
        chat_id,
        user_id
    )

    return member.status in (
        "administrator",
        "owner"
    )


def register_timers(app):

    @app.on_message(
        filters.command("timer") &
        filters.group
    )
    async def timer_handler(
        client,
        message: Message
    ):

        if not await is_admin(
            client,
            message.chat.id,
            message.from_user.id
        ):
            return

        args = message.text.split()

        if len(args) != 3:

            await message.reply_text(
                "Usage:\n"
                "/timer text 60\n"
                "/timer photo 300\n"
                "/timer video 600"
            )
            return

        content_type = args[1].lower()

        if content_type not in VALID_TYPES:

            await message.reply_text(
                "Invalid content type.\n\n"
                f"Available:\n"
                f"{', '.join(VALID_TYPES)}"
            )
            return

        try:
            seconds = int(args[2])
        except ValueError:

            await message.reply_text(
                "Timer must be a number."
            )
            return

        if seconds < 1:

            await message.reply_text(
                "Minimum timer is 1 second."
            )
            return

        if seconds > 604800:

            await message.reply_text(
                "Maximum timer is 604800 seconds "
                "(7 days)."
            )
            return

        await set_timer(
            message.chat.id,
            content_type,
            seconds
        )

        await message.reply_text(
            f"✅ {content_type.upper()} timer "
            f"updated to {seconds} seconds."
        )

    @app.on_message(
        filters.command("status") &
        filters.group
    )
    async def status_handler(
        client,
        message: Message
    ):

        if not await is_admin(
            client,
            message.chat.id,
            message.from_user.id
        ):
            return

        text = await get_status_text(
            message.chat.id
        )

        await message.reply_text(text)
