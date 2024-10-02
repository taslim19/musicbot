from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AashikaMusicBot import app
from config import BOT_USERNAME

start_txt = """**
(っ◔◡◔)っ ♥ ✪ Welcome For dragMusicBot

**"""





@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("𝗔𝗗𝗗 𝗠𝗘", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ],
        [
          InlineKeyboardButton("𝗛𝗘𝗟𝗣", url="https://t.me/updatesdragxmusic"),
          InlineKeyboardButton("𝗢𝗪𝗡𝗘𝗥", url="https://t.me/dragtf"),
          ],
             
[
InlineKeyboardButton("Github", url=f"https://github.com/AryavartX"),

        ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://graph.org/file/1df484ee2b80ec2e2bd2e.jpg",
        caption=start_txt,
        reply_markup=reply_markup
    )
