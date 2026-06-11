import asyncio
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.mongo import jobs

scheduler = AsyncIOScheduler()

BOT = None


def set_bot(bot):
    global BOT
    BOT = bot


async def delete_message(chat_id: int, message_id: int):

    try:
        await BOT.delete_messages(
            chat_id,
            message_id
        )

    except Exception as e:
        print(
            f"Delete failed: {chat_id} "
            f"{message_id} -> {e}"
        )

    await jobs.delete_one(
        {
            "chat_id": chat_id,
            "message_id": message_id
        }
    )


async def schedule_delete(
    chat_id: int,
    message_id: int,
    seconds: int
):

    run_time = (
        datetime.utcnow()
        + timedelta(seconds=seconds)
    )

    await jobs.insert_one(
        {
            "chat_id": chat_id,
            "message_id": message_id,
            "delete_at": run_time
        }
    )

    scheduler.add_job(
        delete_message,
        "date",
        run_date=run_time,
        args=[
            chat_id,
            message_id
        ],
        id=f"{chat_id}_{message_id}",
        replace_existing=True
    )


async def restore_jobs():

    cursor = jobs.find({})

    async for job in cursor:

        chat_id = job["chat_id"]
        message_id = job["message_id"]
        delete_at = job["delete_at"]

        now = datetime.utcnow()

        if delete_at <= now:

            asyncio.create_task(
                delete_message(
                    chat_id,
                    message_id
                )
            )

            continue

        try:

            scheduler.add_job(
                delete_message,
                "date",
                run_date=delete_at,
                args=[
                    chat_id,
                    message_id
                ],
                id=f"{chat_id}_{message_id}",
                replace_existing=True
            )

        except Exception as e:

            print(
                f"Restore failed: "
                f"{message_id} -> {e}"
            )


async def cancel_delete(
    chat_id: int,
    message_id: int
):

    job_id = (
        f"{chat_id}_{message_id}"
    )

    try:
        scheduler.remove_job(job_id)

    except Exception:
        pass

    await jobs.delete_one(
        {
            "chat_id": chat_id,
            "message_id": message_id
        }
    )


async def clear_group_jobs(
    chat_id: int
):

    cursor = jobs.find(
        {
            "chat_id": chat_id
        }
    )

    async for item in cursor:

        job_id = (
            f"{item['chat_id']}_"
            f"{item['message_id']}"
        )

        try:
            scheduler.remove_job(
                job_id
            )
        except Exception:
            pass

    await jobs.delete_many(
        {
            "chat_id": chat_id
        }
    )


def start_scheduler():

    if not scheduler.running:
        scheduler.start()
