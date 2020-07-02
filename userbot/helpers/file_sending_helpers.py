import json
import os.path

from pyrogram import Message

from userbot import UserBotBaseClass
from userbot.helpers.PyroHelpers import ReplyCheck, GetChatID


def reset_file_ids():
    with open("file_ids.txt", "w") as f:
        f.write(json.dumps({}))


if not os.path.exists('file_ids.txt'):
    reset_file_ids()


async def get_old_message(bot: UserBotBaseClass, message_id, media_type):
    old_message = await bot.get_messages('self', message_id)

    if media_type == "photo":
        return old_message.photo

    if media_type == "animation":
        return old_message.animation


# Save the sent media's ID to file to send faster next time
def save_media_id(name, media: Message):
    file_json = json.load(open("file_ids.txt", "r"))
    message_id = media.message_id
    file_json[name] = message_id
    with open("file_ids.txt", "w") as f:
        f.write(json.dumps(file_json))


# Function to reuse to send animation and remember the file_id
async def send_saved_animation(bot: UserBotBaseClass, message: Message, name: str, image: str, caption=None):
    files = json.load(open("file_ids.txt", "r"))

    if name in files:
        old_message = await get_old_message(bot, int(files[name]), "animation")
        if old_message is not None:
            await bot.send_animation(
                message.chat.id,
                old_message.file_id,
                file_ref=old_message.file_ref,
                reply_to_message_id=ReplyCheck(message),
                caption=caption if caption is not None else ''
            )
        else:
            # Reset file id list because of the one error
            reset_file_ids()
            await send_saved_animation(bot, message, name, image, caption)
    else:
        sent_animation = await bot.send_animation(
            "self",
            "userbot/images/{}".format(image),
            reply_to_message_id=ReplyCheck(message)
        )
        save_media_id(name, sent_animation)
        await send_saved_animation(bot, message, name, image, caption)


# Function to reuse to send image and save file_id
async def send_saved_image(bot: UserBotBaseClass, message: Message, name: str, image: str, caption=None):
    files = json.load(open("file_ids.txt", "r"))

    if name in files:
        old_message = await get_old_message(bot, int(files[name]), "photo")
        if old_message is not None:
            await bot.send_photo(
                GetChatID(message),
                old_message.file_id,
                file_ref=old_message.file_ref,
                reply_to_message_id=ReplyCheck(message),
                caption=caption if caption is not None else ''
            )
        else:
            # Reset file id list because of the one error
            reset_file_ids()
            await send_saved_image(bot, message, name, image, caption)
    else:
        sent_photo = await bot.send_photo(
            "self",
            photo="userbot/images/{}".format(image),
            reply_to_message_id=ReplyCheck(message)
        )
        save_media_id(name, sent_photo)
        await send_saved_image(bot, message, name, image, caption)
