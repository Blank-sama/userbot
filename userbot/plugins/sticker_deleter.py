import asyncio

from pyrogram import filters
from pyrogram.types import Message
from Bonten import Bonten
from Bonten.database.sticker_deleter import StickerDeleter
from Bonten.plugins.help import add_command_help


@Bonten.on_message(filters.command("stickerdel", ".") & filters.me)
async def delete_sticker_here(_, message: Message):
    sticker_message = message.reply_to_message
    chat_details = StickerDeleter().find_chat_id(sticker_message)

    if chat_details is not None:

        chat_id = chat_details["chat_id"]
        sticker_id = chat_details['sticker_id']

        if chat_id == message.chat.id and sticker_id == sticker_message.sticker.file_unique_id:
            await message.edit(
                "```Deletion for this sticker enabled here...```"
            )

    elif chat_details is None:
        StickerDeleter().add_sticker_in_chat(sticker_message)
        await message.edit("```Sticker deleter enabled here!!```")

    await asyncio.sleep(2)
    await message.delete()


@Bonten.on_message(filters.command("stickerdel", "!") & filters.me)
async def not_delete_sticker_here(_, message: Message):
    if StickerDeleter().delete_sticker_in_chat(message) is True:
        await message.edit("```Sticker deleter disabled for this chat```")
    else:
        await message.edit("```Sticker deleter was never enabled for this chat```")

    await asyncio.sleep(2)
    await message.delete()


@Bonten.on_message(filters.incoming & filters.sticker)
async def stickered(_, message: Message):
    try:
        chat_details = StickerDeleter().find_chat_id(message) 

        if chat_details is not None: 
            if chat_details["chat_id"] == message.chat.id\
                    and chat_details['sticker_id'] == message.sticker.file_unique_id:
                await message.delete()
    except Exception as e:
        print("Sticker Deleter: MongoDB not configured")


add_command_help(
    "stickerdel",
    [
        [".stickerdel", "Reply to a sticker and the bot will delete it from the chat each time it is sent."],
        ["!stickerdel", "Run the command and it will stop deleting all stickers in a chat."],
    ],
)
