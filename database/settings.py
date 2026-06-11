from database.mongo import groups


DEFAULT_SETTINGS = {
    "delete_text": False,
    "delete_photo": False,
    "delete_video": False,
    "delete_document": False,
    "delete_sticker": False,
    "delete_animation": False,
    "delete_voice": False,
    "delete_audio": False,

    "timer_text": 60,
    "timer_photo": 60,
    "timer_video": 60,
    "timer_document": 60,
    "timer_sticker": 60,
    "timer_animation": 60,
    "timer_voice": 60,
    "timer_audio": 60,
}


async def get_group(group_id: int):
    """
    Get group settings.
    Creates default settings if group doesn't exist.
    """

    data = await groups.find_one(
        {"group_id": group_id}
    )

    if not data:

        data = {
            "group_id": group_id,
            **DEFAULT_SETTINGS
        }

        await groups.insert_one(data)

    return data


async def create_group(group_id: int):
    """
    Create group with default settings.
    """

    exists = await groups.find_one(
        {"group_id": group_id}
    )

    if exists:
        return exists

    data = {
        "group_id": group_id,
        **DEFAULT_SETTINGS
    }

    await groups.insert_one(data)

    return data


async def update_setting(
    group_id: int,
    key: str,
    value
):
    """
    Update a single setting.
    """

    await groups.update_one(
        {"group_id": group_id},
        {
            "$set": {
                key: value
            }
        },
        upsert=True
    )


async def toggle_setting(
    group_id: int,
    key: str
):
    """
    Toggle boolean setting.
    """

    group = await get_group(group_id)

    current = group.get(key, False)

    await groups.update_one(
        {"group_id": group_id},
        {
            "$set": {
                key: not current
            }
        }
    )

    return not current


async def set_timer(
    group_id: int,
    content_type: str,
    seconds: int
):
    """
    Example:
    set_timer(group_id, "photo", 120)
    """

    key = f"timer_{content_type}"

    await groups.update_one(
        {"group_id": group_id},
        {
            "$set": {
                key: seconds
            }
        },
        upsert=True
    )


async def get_timer(
    group_id: int,
    content_type: str
):
    """
    Returns timer for content type.
    """

    group = await get_group(group_id)

    return group.get(
        f"timer_{content_type}",
        60
    )


async def reset_group(group_id: int):
    """
    Reset group to default settings.
    """

    await groups.update_one(
        {"group_id": group_id},
        {
            "$set": DEFAULT_SETTINGS
        },
        upsert=True
    )


async def delete_group(group_id: int):
    """
    Remove group settings from database.
    """

    await groups.delete_one(
        {"group_id": group_id}
    )


async def list_enabled_filters(group_id: int):
    """
    Return all enabled content filters.
    """

    group = await get_group(group_id)

    enabled = []

    for key, value in group.items():

        if key.startswith("delete_") and value:
            enabled.append(key)

    return enabled


async def get_status_text(group_id: int):
    """
    Generate status text for settings panel.
    """

    group = await get_group(group_id)

    return (
        f"📝 Text: {'✅' if group['delete_text'] else '❌'}\n"
        f"🖼 Photo: {'✅' if group['delete_photo'] else '❌'}\n"
        f"🎥 Video: {'✅' if group['delete_video'] else '❌'}\n"
        f"📄 Document: {'✅' if group['delete_document'] else '❌'}\n"
        f"🎭 Sticker: {'✅' if group['delete_sticker'] else '❌'}\n"
        f"🎬 GIF: {'✅' if group['delete_animation'] else '❌'}\n"
        f"🎤 Voice: {'✅' if group['delete_voice'] else '❌'}\n"
        f"🎵 Audio: {'✅' if group['delete_audio'] else '❌'}\n\n"
        f"⏱ Text Timer: {group['timer_text']}s\n"
        f"⏱ Photo Timer: {group['timer_photo']}s\n"
        f"⏱ Video Timer: {group['timer_video']}s\n"
        f"⏱ Document Timer: {group['timer_document']}s\n"
    )
