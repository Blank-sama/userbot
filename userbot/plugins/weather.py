import asyncio
from html import escape

import aiohttp
from pyrogram import Filters, Message

from userbot import UserBot
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command('weather', '.') & Filters.me)
async def weather(bot: UserBot, message: Message):
    if len(message.command) == 1:
        await message.edit("Usage: `.weather Maldives`")
        await asyncio.sleep(3)
        await message.delete()

    if len(message.command) > 1:
        location = message.command[1]
        headers = {'user-agent': 'httpie'}
        url = f"https://wttr.in/{location}?mnTC0&lang=en"
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as resp:
                    data = await resp.text()
        except Exception:
            await message.edit("Failed to get the weather forecast")

        if 'we processed more than 1M requests today' in data:
            await message.edit("`Sorry, we cannot process this request today!`")
        else:
            weather = f"<code>{escape(data)}</code>"
            await message.edit(weather, parse_mode='html')


# Command help section
add_command_help(
    'weather', [
        ['.weather', 'Gets weather information for provided location.'],
    ]
)
