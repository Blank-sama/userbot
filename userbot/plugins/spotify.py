from pyrogram import filters, emoji
from pyrogram.types import Message
from Bonten import UserBot, ALLOWED_USERS
from Bonten.plugins.help import add_command_help

from Bonten.helpers import spotify


@Bonten.on_message(filters.command(["np", "now", "nowplaying"], ".") & (filters.me | filters.user(ALLOWED_USERS)))
async def now_playing(_, message: Message):
    current_track = await spotify.now_playing()

    if not current_track:
        await message.edit("I am not playing any music right now!")
        return

    if current_track == "API details not set":
        await message.edit("API details not set. Please read the README!")
        return

    track = current_track['item']
    song = track['name']
    link = track['external_urls']['spotify']

    await message.edit(f'{emoji.MUSICAL_NOTE} Currently Playing: <a href="{link}">{song}</a>')


@Bonten.on_message(filters.command(["sdev", "sdevices", "spotifydevices", "sd"], ".") & (filters.me | filters.user(ALLOWED_USERS)))
async def list_devices(_, message: Message):
    current_devices = await spotify.list_devices()

    if not current_devices:
        await message.edit("No devices active right now!")
        return

    if current_devices == "API details not set":
        await message.edit("API details not set. Please read the README!")
        return

    devices = ["My devices active on Spotify right now:"]
    for index, device in enumerate(current_devices['devices'], start=1):
        devices.append(f"{index}) {device['name']} - {device['type']}")

    device_msg = '\n'.join(devices)
    await message.edit(device_msg)


@Bonten.on_message(filters.command(["spause", "pause"], ".") & (filters.me))
async def pause(_, message: Message):
    pause = await spotify.pause()
    if pause:
        await message.edit("Spotify playback paused")
    else:
        await message.edit("Nothing is playing on Spotify")

    if pause == "API details not set":
        await message.edit("API details not set. Please read the README!")
        return


@Bonten.on_message(filters.command(["splay", "play"], ".") & (filters.me))
async def play(_, message: Message):
    play = await spotify.play()
    if play:
        await message.edit("Spotify playback started")
    else:
        await message.edit("Playing something already?")

    if play == "API details not set":
        await message.edit("API details not set. Please read the README!")
        return


# Command help section
add_command_help(
    "spotify",
    [
        [
            ".nowplaying | .now | .np",
            "Send your currently playing Spotify song into chat.",
        ],
        [
            ".spotifydevices | .sdevices | .sdev | .sd",
            "Send your Spotify active device list into chat.",
        ],
        [
            ".spause | .pause",
            "Pause your currently playing in Spotify.",
        ],
        [
            ".splay | .play",
            "Resume playback on Spotify",
        ],
    ],
)
