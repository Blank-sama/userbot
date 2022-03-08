from pyrogram import filters
from pyrogram.types import Message
from Bonten import Bonten
from Bonten.plugins.help import add_command_help


@Bonten.on_message(filters.command("s", ".") & filters.me)
async def to_saved(_, message: Message):
    await message.delete()
    await message.reply_to_message.forward("self")


# Command help section
add_command_help(
    "save",
    [
        ["s", "Reply to any message and instantly send it to your saved messages."],
    ],
)
