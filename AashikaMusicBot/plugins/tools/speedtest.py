import logging
import speedtest
from time import time
from AashikaMusicBot.core.utils import edit_or_reply 

# Set up logging
logging.basicConfig(level=logging.INFO)

def convert_from_bytes(size):
    """Convert bytes to a more readable format."""
    power = 2**10
    n = 0
    units = {0: "", 1: "Kbps", 2: "Mbps", 3: "Gbps", 4: "Tbps"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"

async def speedtest_command(update, context):
    """Handle the speed test command."""
    logging.info("Speed test command received")

    input_str = context.args[0] if context.args else ""
    logging.info(f"Input string: {input_str}")

    as_text = input_str == "text"
    as_document = input_str == "file"

    catevent = await edit_or_reply(update, "`Calculating my internet speed. Please wait!`")
    start = time()

    try:
        logging.info("Initializing speed test")
        s = speedtest.Speedtest()
        logging.info("Getting best server")
        s.get_best_server()

        logging.info("Starting download test")
        download_speed = s.download()
        logging.info("Starting upload test")
        upload_speed = s.upload()

        end = time()
        ms = round(end - start, 2)

        logging.info(f"Download Speed: {download_speed}")
        logging.info(f"Upload Speed: {upload_speed}")

        response = s.results.dict()
        ping_time = response.get("ping")
        client_infos = response.get("client")
        i_s_p = client_infos.get("isp")
        i_s_p_rating = client_infos.get("isprating")

        if as_text:
            await catevent.edit(
                f"`SpeedTest completed in {ms} seconds`\n"
                f"`Download: {convert_from_bytes(download_speed)}`\n"
                f"`Upload: {convert_from_bytes(upload_speed)}`\n"
                f"`Ping: {ping_time} ms`\n"
                f"`ISP: {i_s_p}`\n"
                f"`ISP Rating: {i_s_p_rating}`"
            )
        else:
            speedtest_image = s.results.share()
            await update.message.reply_photo(
                photo=speedtest_image,
                caption=f"**SpeedTest** completed in {ms} seconds"
            )

    except Exception as exc:
        logging.error(f"Error during speed test: {str(exc)}")
        await catevent.edit(f"An error occurred: {str(exc)}")

# Ensure to register the command in your bot's main script
