import os
import shutil
from pyrogram import filters
from pyrogram.types import Message

from Bonten import Bonten
from Bonten.helpers.ftp_crawler import get_ftp_files
from Bonten.plugins.help import add_command_help


@Bonten.on_message(filters.command("ftp", ".") & filters.me)
async def ftp_list(bot: Bonten, message: Message):
    await message.edit('Crawling seedbox')

    await get_ftp_files()

    files = []
    for r, _, f in os.walk("downloads/ftp"):
        for file in f:
            files.append(os.path.join(r, file))

        await message.edit(f"{len(files)} files found")

    for f in files:
        await message.reply_chat_action('upload_document')
        await bot.send_document('self', document=f)

    await message.edit("Upload complete")

    shutil.rmtree('downloads/ftp')

add_command_help(
    "ftp",
    [
        [".ftp", "Crawls your ftp and returns file links"],
    ],
)
