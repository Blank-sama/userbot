import asyncio
import time

import speedtest
from pyrogram import filters
from pyrogram.raw import functions
from pyrogram.types import Message

from Bonten import Bonten
from Bonten.helpers.PyroHelpers import SpeedConvert
from Bonten.helpers.constants import WWW
from Bonten.helpers.expand import expand_url
from Bonten.helpers.shorten import shorten_url
from Bonten.plugins.help import add_command_help


@Bonten.on_message(filters.command(["speed", "speedtest"], ".") & filters.me)
async def speed_test(_, message: Message):
    new_msg = await message.edit("`Running speed test . . .`")
    spd = speedtest.Speedtest()

    new_msg = await message.edit(
        f"`{new_msg.text}`\n" "`Getting best server based on ping . . .`"
    )
    spd.get_best_server()

    new_msg = await message.edit(f"`{new_msg.text}`\n" "`Testing download speed . . .`")
    spd.download()

    new_msg = await message.edit(f"`{new_msg.text}`\n" "`Testing upload speed . . .`")
    spd.upload()

    new_msg = await new_msg.edit(
        f"`{new_msg.text}`\n" "`Getting results and preparing formatting . . .`"
    )
    results = spd.results.dict()

    await message.edit(
        WWW.SpeedTest.format(
            start=results["timestamp"],
            ping=results["ping"],
            download=SpeedConvert(results["download"]),
            upload=SpeedConvert(results["upload"]),
            isp=results["client"]["isp"],
        )
    )


@Bonten.on_message(filters.command("dc", ".") & filters.me)
async def nearest_dc(_, message: Message):
    dc = await UserBot.send(functions.help.GetNearestDc())
    await message.edit(WWW.NearestDC.format(dc.country, dc.nearest_dc, dc.this_dc))


@Bonten.on_message(filters.command("ping", ".") & filters.me)
async def ping_me(_, message: Message):
    """Ping the assistant"""
    start = time.time()
    reply = await message.reply_text("...")
    delta_ping = time.time() - start
    await reply.edit_text(f"**Pong!**\n`{delta_ping * 1000:.3f} ms`")


@Bonten.on_message(filters.command("expand", ".") & filters.me)
async def expand(_, message: Message):
    if message.reply_to_message:
        url = message.reply_to_message.text or message.reply_to_message.caption
    elif len(message.command) > 1:
        url = message.command[1]
    else:
        url = None

    if url:
        expanded = await expand_url(url)
        if expanded:
            await message.edit(
                f"<b>Shortened URL</b>: {url}\n<b>Expanded URL</b>: {expanded}",
                disable_web_page_preview=True,
            )
        else:
            await message.edit("No bro that's not what I do")
    else:
        await message.edit("Nothing to expand")


@Bonten.on_message(filters.command("shorten", ".") & filters.me)
async def shorten(_, message: Message):
    keyword = None

    if message.reply_to_message:
        url = message.reply_to_message.text or message.reply_to_message.caption
        if len(message.command) > 1:
            keyword = message.command[1]
    elif len(message.command) > 2:
        url = message.command[1]
        keyword = message.command[2]
    elif len(message.command) > 1:
        url = message.command[1]
    else:
        url = None

    if url:
        shortened = await shorten_url(url, keyword)
        if shortened == "API ERROR":
            txt = "API URL or API KEY not found! Add YOURLS details to config"
        elif shortened == "INVALID URL":
            txt = f"The provided URL: `{url}` is invalid"
        elif shortened == "KEYWORD/URL Exists":
            txt = "The URL or KEYWORD already exists!"
        else:
            txt = f"<b>Original URL</b>: {url}\n<b>Shortened URL</b>: {shortened}"
            await message.edit(txt, disable_web_page_preview=True)
            return
    else:
        txt = "Please provide a URL to shorten"

    await message.edit(txt)
    await asyncio.sleep(3)
    await message.delete()


add_command_help(
    "www",
    [
        [".ping", "Calculates ping time between you and Telegram."],
        [".dc", "Get's your Telegram DC."],
        [
            ".speedtest `or` .speed",
            "Runs a speedtest on the server this userbot is hosted.. Flex on them haters. With an in "
            "Telegram Speedtest of your server..",
        ],
        [
            ".expand",
            "Expands a shortened url. Works for replied to message, photo caption or .expand url",
        ],
        [
            ".shorten",
            "Shortens a url. Works for replied to message, photo caption or .shorten url keyword",
        ],
    ],
)
