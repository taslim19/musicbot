import logging
import speedtest
from time import time
from AashikaMusicBot import plugins # Adjust this import based on your structure
from AashikaMusicBot.core.managers import edit_or_reply  # Ensure this is correct
from AashikaMusicBot.helpers.utils import reply_id  # Ensure this is correct

plugin_category = "utils"

def convert_from_bytes(size):
    power = 2**10
    n = 0
    units = {0: "", 1: "Kbps", 2: "Mbps", 3: "Gbps", 4: "Tbps"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"

@catub.cat_cmd(
    pattern="speedtest(?:\s|$)([\s\S]*)",
    command=("speedtest", plugin_category),
    info={
        "header": "Speedtest for your bot.",
        "options": {
            "text": "will give output as text.",
            "image": "will give output as image (default).",
            "file": "will give output as PNG file.",
        },
        "usage": ["{tr}speedtest <option>", "{tr}speedtest"],
    },
)
async def speedtest_command(event):
    """Speedtest for your bot."""
    input_str = event.pattern_match.group(1)
    as_text = False
    as_document = False

    if input_str == "file":
        as_document = True
    elif input_str == "text":
        as_text = True

    catevent = await edit_or_reply(event, "`Calculating internet speed. Please wait!`")
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
    reply_msg_id = await reply_id(event)

    try:
        speedtest_image = s.results.share()
        if as_text:
            await catevent.edit(
                """`SpeedTest completed in {} seconds`
`Download: {} (or) {} MB/s`
`Upload: {} (or) {} MB/s`
`Ping: {} ms`
`ISP: {}`
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
            await event.client.send_file(
                event.chat_id,
                speedtest_image,
                caption=f"**SpeedTest** completed in {ms} seconds",
                force_document=as_document,
                reply_to=reply_msg_id,
                allow_cache=False,
            )
            await event.delete()
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
