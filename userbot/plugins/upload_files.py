import asyncio

import humanize
from pyrogram import filters
from pyrogram.types import Message

from Bonten import Bonten


async def progress_callback(current, total, bot: UserBot, message: Message):
    if int((current / total) * 100) % 25 == 0:
        await message.edit(f"{humanize.naturalsize(current)} / {humanize.naturalsize(total)}")


@Bonten.on_message(filters.command('upload', '.') & filters.me)
async def upload_helper(bot: UserBot, message: Message):
    if len(message.command) > 1:
        await bot.send_document('self', message.command[1], progress=progress_callback, progress_args=(bot, message))
    else:
        await message.edit('No path provided.')
        await asyncio.sleep(3)

    await message.delete()
