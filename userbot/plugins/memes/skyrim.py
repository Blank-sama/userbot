import asyncio
import os
import time

from pyrogram import filters
from pyrogram.types import Message
from Bonten import Bonten
from Bonten.helpers.PyroHelpers import ReplyCheck
from Bonten.plugins.help import add_command_help


@Bonten.on_message(filters.command(["skyrim", "skill"], ".") & filters.me)
async def skyrim(bot: Bonten, message: Message):
    if len(message.command) >= 2:
        text = message.command[1]
    else:
        await message.edit("```Not enough params```")
        await asyncio.sleep(3)
        await message.delete()
        return

    level = message.command[2] if len(message.command) >= 3 else 100

    try:
        try:
            if os.name == "nt":
                os.system(
                    f'venv\\Scripts\\activate && python Bonten\\helpers\\skyrim.py "{text}" {level}'
                )
            else:
                os.system(
                    f'. venv/bin/activate && python Bonten//helpers//skyrim.py "{text}" {level}'
                )
        except Exception:
            await message.edit("```Failed to generate skill```")
            time.sleep(2)
            await message.delete()

        try:
            await bot.send_photo(
                message.chat.id,
                "Bonten/downloads/skyrim.png",
                reply_to_message_id=ReplyCheck(message),
            )
            await message.delete()
        except Exception:
            await message.edit("```Failed to send skill```")
            time.sleep(2)
            await message.delete()
        finally:
            os.remove("Bonten/downloads/skyrim.png")
    except Exception as e:
        print(e)


# Command help section
add_command_help(
    "skyrim",
    [
        [".skyrim", "Generate skyrim skill image.\n .skyrim <before> <after>"],
        [".skill", "Generate skyrim skill image.\n .skill <before> <after>"],
    ],
)
