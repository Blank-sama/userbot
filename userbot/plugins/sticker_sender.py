from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import ChatSendStickersForbidden
from Bonten import Bonten

SETS = {
    1: [
        'CAACAgUAAxkDAAI4IGEOvOVBnkzKf6MQCgvsJuGk5PRbAAKYAgACf1BBV4xU-M-oahBJHgQ',
        'CAACAgUAAxkDAAI4IWEOvOZKgAYskiJ3gcu6InBogwnkAAJKAwACmd1BV4c0knnsItszHgQ',
        'CAACAgUAAxkDAAI4ImEOvOmcilCfnLmTxOGZj5Liv0t5AAIVBAACvM9BV9WweboNia0rHgQ'
    ],
    2: [
        'CAACAgUAAxkDAAI4J2EOvtgOW67X-ozbSRS_0ubjEJEMAAIbAwACcYtQV1-l_18Yq80SHgQ',
        'CAACAgUAAxkDAAI4KGEOvtnG2TMNUKYOLkof4g0Yp5hSAAJKAgACGM5RV20DZ7YyvyeCHgQ',
        'CAACAgUAAxkDAAI4KWEOvtkP_NTgkg4GobiDa9pNJPfXAAI9AwACrd9RVx3nZiYeQ4PeHgQ'
    ]
}


@Bonten.on_message(filters.command(["sticker"], ".") & filters.me)
async def sticker_sender(bot: Bonten, message: Message):
    if len(message.command) > 1:
        set_to_send = message.command[1]

        if type(set_to_send) == str:
            set_to_send = int(set_to_send)

        stickers = SETS[set_to_send]

        for x in stickers:
            try:
                await bot.send_sticker(message.chat.id, x)
            except ChatSendStickersForbidden:
                await message.edit("```Cannot send stickers here```")
                await message.delete()
                return

        await message.delete()


# @Bonten.on_message(filters.sticker & filters.me)
# async def sticker_sender(_, message: Message):
#     print(message.sticker.file_id)
