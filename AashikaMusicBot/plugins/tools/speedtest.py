import logging
import speedtest
from time import time
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from AashikaMusicBot import app
from AashikaMusicBot.misc import SUDOERS
from AashikaMusicBot.utils.decorators.language import language

plugin_category = "utils"

def convert_from_bytes(size):
    power = 2**10
    n = 0
    units = {0: "", 1: "Kbps", 2: "Mbps", 3: "Gbps", 4: "Tbps"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"

# Replace this with your actual command handler
async def speedtest_command(update, context):
    input_str = context.args[0] if context.args else ""
    as_text = False
    as_document = False
    if input_str == "file":
        as_document = True
    elif input_str == "image":
        as_document = False
    elif input_str == "text":
        as_text = True
    
    catevent = await edit_or_reply(update, "`Calculating my internet speed. Please wait!`")
    start = time()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = time()
    ms = round(end - start, 2)
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")
    reply_msg_id = await reply_id(update)

    try:
        speedtest_image = s.results.share()
        if as_text:
            await catevent.edit(
                """`SpeedTest completed in {} seconds`

`Download: {} (or) {} MB/s`
`Upload: {} (or) {} MB/s`
`Ping: {} ms`
`Internet Service Provider: {}`
`ISP Rating: {}`""".format(
                    ms,
                    convert_from_bytes(download_speed),
                    round(download_speed / 8e6, 2),
                    convert_from_bytes(upload_speed),
                    round(upload_speed / 8e6, 2),
                    ping_time,
                    i_s_p,
                    i_s_p_rating,
                )
            )
        else:
            await update.message.reply_photo(
                photo=speedtest_image,
                caption=f"**SpeedTest** completed in {ms} seconds",
                reply_to_message_id=reply_msg_id
            )

            await update.message.delete()
    except Exception as exc:
        await catevent.edit(
            """**SpeedTest** completed in {} seconds
Download: {} (or) {} MB/s
Upload: {} (or) {} MB/s
Ping: {} ms

__With the Following ERRORs__
{}""".format(
                ms,
                convert_from_bytes(download_speed),
                round(download_speed / 8e6, 2),
                convert_from_bytes(upload_speed),
                round(upload_speed / 8e6, 2),
                ping_time,
                str(exc),
            )
        )

# Make sure to register this command in your bot's command handler
