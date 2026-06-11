from pyrogram import filters
from pyrogram.types import Message

from database.settings import (
    get_group,
    get_timer
)

from utils.scheduler import (
    schedule_delete
)


async def should_delete(
    group_id: int,
    content_type: str
):

    settings = await get_group(
        group_id
    )

    return settings.get(
        f"delete_{content_type}",
        False
    )


async def process_message(
    message: Message,
    content_type: str
):

    group_id = message.chat.id

    enabled = await should_delete(
        group_id,
        content_type
    )

    if not enabled:
        return

    timer = await get_timer(
        group_id,
        content_type
    )

    await schedule_delete(
        chat_id=group_id,
        message_id=message.id,
        seconds=timer
    )


def register_messages(app):

    # TEXT

    @app.on_message(
        filters.group &
        filters.text
    )
    async def text_handler(
        client,
        message: Message
    ):

        if not message.from_user:
            return

        await process_message(
            message,
            "text"
        )

    # PHOTO

    @app.on_message(
        filters.group &
        filters.photo
    )
    async def photo_handler(
        client,
        message: Message
    ):

        await process_message(
            message,
            "photo"
        )

    # VIDEO

    @app.on_message(
        filters.group &
        filters.video
    )
    async def video_handler(
        client,
        message: Message
    ):

        await process_message(
            message,
            "video"
        )

    # DOCUMENT

    @app.on_message(
        filters.group &
        filters.document
    )
    async def document_handler(
        client,
        message: Message
    ):

        await process_message(
            message,
            "document"
        )

    # STICKER

    @app.on_message(
        filters.group &
        filters.sticker
    )
    async def sticker_handler(
        client,
        message: Message
    ):

        await process_message(
            message,
            "sticker"
        )

    # GIF / Animation

    @app.on_message(
        filters.group &
        filters.animation
    )
    async def animation_handler(
        client,
        message: Message
    ):

        await process_message(
            message,
            "animation"
        )

    # VOICE

    @app.on_message(
        filters.group &
        filters.voice
    )
    async def voice_handler(
        client,
        message: Message
    ):

        await process_message(
            message,
            "voice"
        )

    # AUDIO

    @app.on_message(
        filters.group &
        filters.audio
    )
    async def audio_handler(
        client,
        message: Message
    ):

        await process_message(
            message,
            "audio"
        )
