import asyncio
import importlib
import psutil
import subprocess
from pyrogram import idle, Client, filters
from pytgcalls.exceptions import NoActiveGroupCall

import config
from AashikaMusicBot import LOGGER, app, userbot
from AashikaMusicBot.core.call import AashikaMusicBot
from AashikaMusicBot.misc import sudo
from AashikaMusicBot.plugins import ALL_MODULES
from AashikaMusicBot.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# Replace with your owner ID
OWNER_ID = 7058357442  # Your Telegram user ID

def get_system_stats():
    try:
        uptime = subprocess.check_output("uptime -p", shell=True).decode().strip()
        print(f"Uptime: {uptime}")  # Debug output
    except Exception as e:
        uptime = f"Error fetching uptime: {str(e)}"
        print(uptime)  # Debug output

    try:
        ram = psutil.virtual_memory()
        ram_info = (f"Total: {ram.total / (1024 ** 2):.2f} MB, "
                     f"Used: {ram.used / (1024 ** 2):.2f} MB, "
                     f"Free: {ram.free / (1024 ** 2):.2f} MB")
        print(f"RAM Info: {ram_info}")  # Debug output
    except Exception as e:
        ram_info = f"Error fetching RAM info: {str(e)}"
        print(ram_info)  # Debug output

    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        print(f"CPU Usage: {cpu_usage}%")  # Debug output
    except Exception as e:
        cpu_usage = f"Error fetching CPU usage: {str(e)}"
        print(cpu_usage)  # Debug output

    try:
        disk = psutil.disk_usage('/')
        disk_info = (f"Total: {disk.total / (1024 ** 3):.2f} GB, "
                     f"Used: {disk.used / (1024 ** 3):.2f} GB, "
                     f"Free: {disk.free / (1024 ** 3):.2f} GB")
        print(f"Disk Info: {disk_info}")  # Debug output
    except Exception as e:
        disk_info = f"Error fetching Disk info: {str(e)}"
        print(disk_info)  # Debug output

    tg_calls_status = "Running"  # Replace with actual check if necessary

    return (f"**System Stats:**\n\n"
            f"**Uptime:** {uptime}\n"
            f"**RAM:** {ram_info}\n"
            f"**CPU Usage:** {cpu_usage}%\n"
            f"**Disk Usage:** {disk_info}\n"
            f"**Py-TgCalls Status:** {tg_calls_status}")
@bot.on_message(filters.command('splay'))
def handle_splay(client, message):
    try:
        track_link = message.text.split(" ", 1)[1]  # Get the Spotify link
        spotify_api = SpotifyAPI()

        track_details = await spotify_api.play_track(track_link)
        if track_details:
            await play_track(track_details['link'])  # Implement play_track for actual playback
            await message.reply(f"Now playing from Spotify: {track_details['title']}")
        else:
            await message.reply("Track not found on Spotify.")
    except IndexError:
        await message.reply("Please provide a Spotify track link after /splay.")


@app.on_message(filters.command("ping") & filters.user(OWNER_ID))
async def ping_command(client, message):
    stats = get_system_stats()
    await message.reply_text(stats)

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐀 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐒𝐞𝐬𝐬𝐢𝐨𝐧")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("AashikaMusicBot.plugins" + all_module)
    LOGGER("AashikaMusicBot.plugins").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")
    await userbot.start()
    await AashikaMusicBot.start()
    try:
        await AashikaMusicBot.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("AashikaMusicBot").error(
            "𝗣𝗹𝗫 𝗦𝗧𝗔𝗥𝗧 𝗬𝗢𝗨𝗥 𝗟𝗢𝗚 𝗚𝗥𝗢𝗨𝗣 𝗩𝗢𝗜𝗖𝗘𝗖𝗛𝗔𝗧\𝗖𝗛𝗔𝗡𝗡𝗘𝗟\n\n𝐀𝐍𝐍𝐚𝔶𝐚𝐍ⓧ 𝗕𝗢𝗧 𝗦𝗧𝗢𝗣........"
        )
        exit()
    except:
        pass
    await AashikaMusicBot.decorators()
    LOGGER("AashikaMusicBot").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  Made By AryavartX☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("AashikaMusicBot").info("𝗦𝗧𝗢𝗣 A 𝗠𝗨𝗦𝗜𝗖🎻 𝗕𝗢𝗧..")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
