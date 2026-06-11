from pyrogram import filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.settings import (
    get_status_text,
    toggle_setting
)


def settings_keyboard():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📝 Text",
                    callback_data="toggle_text"
                ),
                InlineKeyboardButton(
                    "🖼 Photo",
                    callback_data="toggle_photo"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎥 Video",
                    callback_data="toggle_video"
                ),
                InlineKeyboardButton(
                    "📄 Document",
                    callback_data="toggle_document"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎭 Sticker",
                    callback_data="toggle_sticker"
                ),
                InlineKeyboardButton(
                    "🎬 GIF",
                    callback_data="toggle_animation"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎤 Voice",
                    callback_data="toggle_voice"
                ),
                InlineKeyboardButton(
                    "🎵 Audio",
                    callback_data="toggle_audio"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔄 Refresh",
                    callback_data="refresh_settings"
                )
            ]
        ]
    )


async def is_admin(client, chat_id, user_id):

    member = await client.get_chat_member(
        chat_id,
        user_id
    )

    return member.status in (
        "administrator",
        "owner"
    )


def register_settings(app):

    @app.on_message(
        filters.command("settings") &
        filters.group
    )
    async def settings_handler(
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

        await message.reply_text(
            text,
            reply_markup=settings_keyboard()
        )

    @app.on_callback_query(
        filters.regex("^toggle_")
    )
    async def toggle_callback(
        client,
        callback: CallbackQuery
    ):

        user = callback.from_user

        if not await is_admin(
            client,
            callback.message.chat.id,
            user.id
        ):
            await callback.answer(
                "Admins only",
                show_alert=True
            )
            return

        key = callback.data.replace(
            "toggle_",
            "delete_"
        )

        await toggle_setting(
            callback.message.chat.id,
            key
        )

        text = await get_status_text(
            callback.message.chat.id
        )

        await callback.message.edit_text(
            text,
            reply_markup=settings_keyboard()
        )

        await callback.answer(
            "Updated"
        )

    @app.on_callback_query(
        filters.regex("^refresh_settings$")
    )
    async def refresh_callback(
        client,
        callback: CallbackQuery
    ):

        text = await get_status_text(
            callback.message.chat.id
        )

        await callback.message.edit_text(
            text,
            reply_markup=settings_keyboard()
        )

        await callback.answer()
