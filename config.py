import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN")
# Add Owner Username without @ 
OWNER_USERNAME = getenv("OWNER_USERNAME","Drag")
# Get Your bot username
BOT_USERNAME = getenv("BOT_USERNAME" , "DragMusicBot")
# Don't Add style font 
BOT_NAME = getenv("BOT_NAME" , "Drag Music")
#get Your Assistant User name
ASSUSERNAME = getenv("ASSUSERNAME" , "DragMusicAssistant")
EVALOP = list(map(int, getenv("EVALOP","7058357442").split()))

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", None)
DEEP_API = getenv("DEEP_API","84c2b291-62fc-4358-b6c1-768317d84a1b")
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 9999999))

# Chat id of a group for logging bot's activities
LOGGER_ID = "@dragxmusiclogs"

# Get this value from  on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", 5413711986))

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/AryavartX/AryavartMusic",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/updatesdragxmusic")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/dragbackup")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))


# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "48037b43459c4bacbce6c61be2575ade")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "103c89540301422aa880a462ca556416")


# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))


# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 5242880000))
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes



STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}


START_IMG_URL = getenv(
    "START_IMG_URL", "https://graph.org/file/1df484ee2b80ec2e2bd2e.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://graph.org/file/0dfcbd2935f41b21af907.jpg"
)
PLAYLIST_IMG_URL = "https://telegra.ph/file/e02fcc6bbfa0a882d6c8b.jpg"
STATS_IMG_URL = "https://telegra.ph/file/e02fcc6bbfa0a882d6c8b.jpg"
TELEGRAM_AUDIO_URL = "https://telegra.ph/file/e02fcc6bbfa0a882d6c8b.jpg"
TELEGRAM_VIDEO_URL = "https://telegra.ph/file/e02fcc6bbfa0a882d6c8b.jpg"
STREAM_IMG_URL = "https://telegra.ph/file/e02fcc6bbfa0a882d6c8b.jpg"
SOUNCLOUD_IMG_URL = "https://telegra.ph/file/e02fcc6bbfa0a882d6c8b.jpg"
YOUTUBE_IMG_URL = "https://telegra.ph/file/e02fcc6bbfa0a882d6c8b.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://telegra.ph/file/e02fcc6bbfa0a882d6c8b.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://telegra.ph/file/e02fcc6bbfa0a882d6c8b.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://telegra.ph/file/e02fcc6bbfa0a882d6c8b.jpg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
